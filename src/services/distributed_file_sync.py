"""
Distributed File System Synchronization for Platinum Tier
Synchronizes files across multiple regions with conflict resolution and quantum-safe encryption
"""
import os
import hashlib
import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import shutil
from enum import Enum
import asyncio
import aiofiles
from ..utils.quantum_resistant_hash import QuantumResistantHasher
from ..utils.quantum_security import QuantumSafeEncryption


class SyncStatus(Enum):
    PENDING = "pending"
    SYNCING = "syncing"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFLICT = "conflict"


class ConflictResolutionStrategy(Enum):
    LAST_WRITE_WINS = "last_write_wins"
    MANUAL_RESOLUTION = "manual_resolution"
    MERGE_IF_POSSIBLE = "merge_if_possible"
    CUSTOM_RULES = "custom_rules"


@dataclass
class FileMetadata:
    """Metadata for synchronized files"""
    path: str
    size: int
    hash: str
    last_modified: float
    created_at: float
    version: int
    region: str
    replicas: List[str]  # List of regions where file is replicated


@dataclass
class SyncOperation:
    """Represents a file synchronization operation"""
    source_path: str
    destination_path: str
    operation_type: str  # 'upload', 'download', 'delete', 'update'
    status: SyncStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class DistributedFileSyncService:
    """
    Distributed file synchronization service with quantum-safe encryption
    """

    def __init__(self, regions: List[str], base_path: str = "./distributed_storage"):
        self.regions = regions
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

        # Quantum-safe encryption for file transfer
        self.qse = QuantumSafeEncryption()
        self.hasher = QuantumResistantHasher()

        # Local storage for each region
        self.region_paths = {}
        for region in regions:
            region_path = self.base_path / region
            region_path.mkdir(exist_ok=True)
            self.region_paths[region] = region_path

        # Metadata storage
        self.metadata_file = self.base_path / "metadata.json"
        self.file_metadata = self._load_metadata()

        # Active sync operations
        self.active_operations: Dict[str, SyncOperation] = {}
        self.sync_lock = threading.Lock()

        # Configuration
        self.conflict_resolution_strategy = ConflictResolutionStrategy.LAST_WRITE_WINS
        self.encryption_enabled = True
        self.replication_factor = 3  # Number of copies to maintain

    def _load_metadata(self) -> Dict[str, FileMetadata]:
        """Load file metadata from persistent storage"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)
                # Convert dict back to FileMetadata objects
                return {
                    path: FileMetadata(
                        path=item['path'],
                        size=item['size'],
                        hash=item['hash'],
                        last_modified=item['last_modified'],
                        created_at=item['created_at'],
                        version=item['version'],
                        region=item['region'],
                        replicas=item['replicas']
                    )
                    for path, item in data.items()
                }
        return {}

    def _save_metadata(self):
        """Save file metadata to persistent storage"""
        data = {
            path: {
                'path': meta.path,
                'size': meta.size,
                'hash': meta.hash,
                'last_modified': meta.last_modified,
                'created_at': meta.created_at,
                'version': meta.version,
                'region': meta.region,
                'replicas': meta.replicas
            }
            for path, meta in self.file_metadata.items()
        }
        with open(self.metadata_file, 'w') as f:
            json.dump(data, f, indent=2)

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate quantum-resistant hash of a file"""
        with open(file_path, 'rb') as f:
            file_content = f.read()
        hash_result = self.hasher.hash(file_content)
        return hash_result.digest

    def get_file_metadata(self, file_path: str, region: str) -> FileMetadata:
        """Get metadata for a file"""
        path_obj = Path(file_path)
        stat = path_obj.stat()

        return FileMetadata(
            path=file_path,
            size=stat.st_size,
            hash=self.calculate_file_hash(path_obj),
            last_modified=stat.st_mtime,
            created_at=stat.st_ctime,
            version=1,  # This would be incremented for each update
            region=region,
            replicas=[region]  # Initially only in current region
        )

    def register_file(self, file_path: str, region: str) -> FileMetadata:
        """Register a file in the synchronization system"""
        metadata = self.get_file_metadata(file_path, region)
        self.file_metadata[file_path] = metadata
        self._save_metadata()
        return metadata

    def sync_file_to_regions(self, source_file: str, target_regions: Optional[List[str]] = None) -> bool:
        """
        Synchronize a file to specified regions (or all regions if None)

        Args:
            source_file: Path to source file
            target_regions: List of regions to sync to (None = all regions)

        Returns:
            True if sync succeeded, False otherwise
        """
        if target_regions is None:
            target_regions = self.regions

        source_path = Path(source_file)
        if not source_path.exists():
            return False

        source_region = self._get_file_region(source_file)
        if not source_region:
            # If file isn't registered, register it in the current region
            source_region = self.regions[0]  # Default to first region
            self.register_file(source_file, source_region)

        # Encrypt file if encryption is enabled
        if self.encryption_enabled:
            encrypted_file = self._encrypt_file(source_file)
        else:
            encrypted_file = source_file

        success_count = 0
        total_targets = len(target_regions)

        for target_region in target_regions:
            if target_region == source_region:
                continue  # Skip source region

            target_path = self.region_paths[target_region] / Path(source_file).name

            try:
                # Check if target file exists and handle conflicts
                if target_path.exists():
                    target_hash = self.calculate_file_hash(target_path)
                    source_hash = self.file_metadata[source_file].hash

                    if source_hash != target_hash:
                        # Conflict detected - handle according to strategy
                        if not self._handle_conflict(source_file, str(target_path), source_hash, target_hash):
                            continue  # Skip this sync

                # Copy file to target region
                shutil.copy2(encrypted_file, target_path)

                # Update metadata
                if source_file in self.file_metadata:
                    self.file_metadata[source_file].replicas.append(target_region)
                    self._save_metadata()

                success_count += 1

            except Exception as e:
                print(f"Failed to sync {source_file} to {target_region}: {str(e)}")
                continue

        return success_count == total_targets - 1  # All targets except source

    def _encrypt_file(self, file_path: str) -> str:
        """Encrypt a file using quantum-safe encryption"""
        # Generate a temporary encrypted file
        temp_encrypted = Path(file_path).with_suffix('.enc.tmp')

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate a quantum-safe key
        key, salt, algorithm = self.qse.generate_quantum_safe_key()

        # Encrypt the content
        encrypted_data = self.qse.encrypt(content, key)

        # Save encrypted data with metadata
        encrypted_package = {
            'data': encrypted_data,
            'salt': salt,
            'algorithm': algorithm,
            'original_path': file_path
        }

        with open(temp_encrypted, 'w', encoding='utf-8') as f:
            json.dump(encrypted_package, f)

        return str(temp_encrypted)

    def _handle_conflict(self, source_file: str, target_file: str, source_hash: str, target_hash: str) -> bool:
        """Handle file conflicts according to configured strategy"""
        if self.conflict_resolution_strategy == ConflictResolutionStrategy.LAST_WRITE_WINS:
            # Compare modification times and keep the most recent
            source_time = self.file_metadata[source_file].last_modified
            target_time = os.path.getmtime(target_file)

            if source_time > target_time:
                # Source is newer, overwrite target
                return True
            else:
                # Target is newer, don't sync
                return False

        elif self.conflict_resolution_strategy == ConflictResolutionStrategy.MANUAL_RESOLUTION:
            # For now, just return False to prevent automatic overwrites
            print(f"Conflict detected between {source_file} and {target_file}. Manual resolution required.")
            return False

        elif self.conflict_resolution_strategy == ConflictResolutionStrategy.MERGE_IF_POSSIBLE:
            # Attempt to merge if both are text files
            return self._attempt_merge(source_file, target_file)

        else:  # CUSTOM_RULES
            # Apply custom rules (placeholder)
            return True

    def _attempt_merge(self, source_file: str, target_file: str) -> bool:
        """Attempt to merge two files if possible"""
        try:
            # Try to read both as text files
            with open(source_file, 'r', encoding='utf-8') as sf:
                source_lines = sf.readlines()

            with open(target_file, 'r', encoding='utf-8') as tf:
                target_lines = tf.readlines()

            # Simple merge strategy: append target lines that aren't in source
            merged_lines = source_lines[:]
            for line in target_lines:
                if line not in merged_lines:
                    merged_lines.append(line)

            # Write merged content back to source
            with open(source_file, 'w', encoding='utf-8') as sf:
                sf.writelines(merged_lines)

            return True

        except UnicodeDecodeError:
            # Not text files, can't merge
            return False
        except Exception:
            return False

    def _get_file_region(self, file_path: str) -> Optional[str]:
        """Get the primary region for a file"""
        if file_path in self.file_metadata:
            return self.file_metadata[file_path].region
        return None

    def replicate_file(self, file_path: str, replication_factor: Optional[int] = None) -> bool:
        """
        Replicate a file to achieve the desired replication factor

        Args:
            file_path: Path to file to replicate
            replication_factor: Number of replicas to maintain (None = use default)

        Returns:
            True if replication succeeded, False otherwise
        """
        if replication_factor is None:
            replication_factor = self.replication_factor

        if file_path not in self.file_metadata:
            print(f"File {file_path} not registered in synchronization system")
            return False

        current_replicas = len(self.file_metadata[file_path].replicas)

        if current_replicas >= replication_factor:
            return True  # Already sufficient replicas

        # Select regions that don't have the file yet
        available_regions = [r for r in self.regions if r not in self.file_metadata[file_path].replicas]
        regions_to_sync = available_regions[:replication_factor - current_replicas]

        return self.sync_file_to_regions(file_path, regions_to_sync)

    def sync_all_files(self) -> Dict[str, bool]:
        """
        Synchronize all registered files across all regions

        Returns:
            Dictionary mapping file paths to sync success status
        """
        results = {}
        for file_path in list(self.file_metadata.keys()):
            results[file_path] = self.sync_file_to_regions(file_path)
        return results

    def get_replication_status(self, file_path: str) -> Dict[str, any]:
        """
        Get replication status for a specific file

        Args:
            file_path: Path to file

        Returns:
            Dictionary with replication status information
        """
        if file_path not in self.file_metadata:
            return {"error": "File not registered"}

        metadata = self.file_metadata[file_path]
        expected_replicas = min(len(self.regions), self.replication_factor)
        actual_replicas = len(metadata.replicas)

        return {
            "file_path": file_path,
            "primary_region": metadata.region,
            "expected_replicas": expected_replicas,
            "actual_replicas": actual_replicas,
            "replica_locations": metadata.replicas,
            "is_fully_replicated": actual_replicas >= expected_replicas,
            "missing_replicas": [r for r in self.regions if r not in metadata.replicas]
        }

    def cleanup_temporary_files(self):
        """Clean up temporary encrypted files"""
        for region_path in self.region_paths.values():
            for temp_file in region_path.glob("*.enc.tmp"):
                temp_file.unlink()


# Example usage and testing
if __name__ == "__main__":
    # Initialize the distributed file sync service
    regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
    sync_service = DistributedFileSyncService(regions)

    print("Testing Distributed File Synchronization Service...")

    # Create a sample file to synchronize
    sample_file = "./sample_document.txt"
    with open(sample_file, 'w') as f:
        f.write("This is a sample document for distributed synchronization testing.\n")
        f.write(f"Created at: {datetime.now().isoformat()}\n")
        f.write("This file will be synchronized across multiple regions.\n")

    # Register the file
    metadata = sync_service.register_file(sample_file, "us-east-1")
    print(f"Registered file: {metadata.path} with hash: {metadata.hash[:16]}...")

    # Replicate the file
    replication_success = sync_service.replicate_file(sample_file)
    print(f"Replication success: {replication_success}")

    # Check replication status
    status = sync_service.get_replication_status(sample_file)
    print(f"Replication status: {status}")

    # Sync all files
    all_results = sync_service.sync_all_files()
    print(f"Sync results: {all_results}")

    # Cleanup temporary files
    sync_service.cleanup_temporary_files()
    print("Temporary files cleaned up.")

    # Clean up sample file
    if os.path.exists(sample_file):
        os.remove(sample_file)
        print("Sample file cleaned up.")