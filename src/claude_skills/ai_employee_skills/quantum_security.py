"""
Quantum Key Management System for Platinum Tier
Manages the lifecycle of quantum-safe cryptographic keys
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import secrets
import hashlib


class QuantumSecurityLevel(Enum):
    BASIC = "basic"
    ENHANCED = "enhanced"
    QUANTUM_SAFE = "quantum_safe"


class KeyType(Enum):
    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"


@dataclass
class QuantumKey:
    """Represents a quantum-safe cryptographic key"""
    id: str
    key_type: str
    algorithm: str
    security_level: str
    generation_date: str
    expiration_date: Optional[str]
    rotation_interval_hours: int
    status: str
    quantum_entropy_source: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any]


class QuantumKeyManagementSystem:
    """
    Quantum key management system with rotation and lifecycle management
    """

    def __init__(self, storage_path: str = "./quantum_keys"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.keys_dir = self.storage_path / "keys"
        self.keys_dir.mkdir(exist_ok=True)
        self.metadata_file = self.storage_path / "key_registry.json"

        # Initialize registry
        if not self.metadata_file.exists():
            self.registry = {"keys": {}}
            self._save_registry()
        else:
            with open(self.metadata_file, 'r') as f:
                self.registry = json.load(f)

    def generate_quantum_key(
        self,
        key_type: KeyType = KeyType.SYMMETRIC,
        security_level: QuantumSecurityLevel = QuantumSecurityLevel.QUANTUM_SAFE,
        algorithm: str = "lattice-based",
        rotation_interval_hours: int = 24
    ) -> str:
        """
        Generate a new quantum-safe key

        Args:
            key_type: Type of key to generate
            security_level: Security level for the key
            algorithm: Cryptographic algorithm to use
            rotation_interval_hours: Hours between key rotations

        Returns:
            ID of the generated key
        """
        key_id = str(uuid.uuid4())

        # Generate quantum-safe key material based on security level
        if security_level == QuantumSecurityLevel.BASIC:
            key_size = 256  # bits
        elif security_level == QuantumSecurityLevel.ENHANCED:
            key_size = 384  # bits
        else:  # QUANTUM_SAFE
            key_size = 512  # bits

        # Generate key material using quantum-safe entropy source
        key_material = secrets.token_bytes(key_size // 8)

        # Create key record
        now = datetime.utcnow().isoformat() + "Z"
        expiration = (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z"  # 1 year expiry

        key_record = QuantumKey(
            id=key_id,
            key_type=key_type.value,
            algorithm=algorithm,
            security_level=security_level.value,
            generation_date=now,
            expiration_date=expiration,
            rotation_interval_hours=rotation_interval_hours,
            status="active",
            quantum_entropy_source="hardware_random_number_generator",
            created_at=now,
            updated_at=now,
            metadata={
                "size_bits": key_size,
                "usage_count": 0,
                "last_rotation": now,
                "next_rotation_due": (
                    datetime.utcnow() + timedelta(hours=rotation_interval_hours)
                ).isoformat() + "Z"
            }
        )

        # Save key material to file
        key_file_path = self.keys_dir / f"{key_id}.key"
        with open(key_file_path, 'wb') as f:
            f.write(key_material)

        # Register key in registry
        self.registry["keys"][key_id] = asdict(key_record)
        self._save_registry()

        return key_id

    def get_key(self, key_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a key's metadata

        Args:
            key_id: ID of the key to retrieve

        Returns:
            Key metadata dictionary or None if not found
        """
        return self.registry["keys"].get(key_id)

    def get_key_material(self, key_id: str) -> Optional[bytes]:
        """
        Retrieve the actual key material (should only be used for encryption/decryption)

        Args:
            key_id: ID of the key to retrieve

        Returns:
            Raw key bytes or None if not found
        """
        key_file_path = self.keys_dir / f"{key_id}.key"
        if key_file_path.exists():
            with open(key_file_path, 'rb') as f:
                return f.read()
        return None

    def list_keys(self) -> List[Dict[str, Any]]:
        """
        List all keys in the system

        Returns:
            List of key metadata dictionaries
        """
        return list(self.registry["keys"].values())

    def rotate_key(self, key_id: str) -> bool:
        """
        Rotate a key by generating a new one with the same ID

        Args:
            key_id: ID of the key to rotate

        Returns:
            True if rotation succeeded, False otherwise
        """
        if key_id not in self.registry["keys"]:
            return False

        # Mark old key as rotated
        old_key = self.registry["keys"][key_id]
        old_key["status"] = "rotated"
        old_key["updated_at"] = datetime.utcnow().isoformat() + "Z"

        # Generate new key with same properties
        new_key_id = self.generate_quantum_key(
            key_type=KeyType(old_key["key_type"]),
            security_level=QuantumSecurityLevel(old_key["security_level"]),
            algorithm=old_key["algorithm"],
            rotation_interval_hours=old_key["rotation_interval_hours"]
        )

        # Update registry to point to new key
        self.registry["keys"][key_id] = self.registry["keys"][new_key_id]
        del self.registry["keys"][new_key_id]  # Remove temp entry

        # Update metadata
        now = datetime.utcnow().isoformat() + "Z"
        self.registry["keys"][key_id]["id"] = key_id
        self.registry["keys"][key_id]["status"] = "active"
        self.registry["keys"][key_id]["updated_at"] = now
        self.registry["keys"][key_id]["metadata"]["last_rotation"] = now
        self.registry["keys"][key_id]["metadata"]["next_rotation_due"] = (
            datetime.utcnow() + timedelta(hours=old_key["rotation_interval_hours"])
        ).isoformat() + "Z"

        self._save_registry()
        return True

    def revoke_key(self, key_id: str) -> bool:
        """
        Revoke a key by marking it as inactive

        Args:
            key_id: ID of the key to revoke

        Returns:
            True if revocation succeeded, False otherwise
        """
        if key_id not in self.registry["keys"]:
            return False

        self.registry["keys"][key_id]["status"] = "revoked"
        self.registry["keys"][key_id]["updated_at"] = datetime.utcnow().isoformat() + "Z"
        self._save_registry()
        return True

    def cleanup_expired_keys(self) -> List[str]:
        """
        Clean up expired keys

        Returns:
            List of cleaned up key IDs
        """
        cleaned_keys = []
        now = datetime.utcnow()

        for key_id, key_data in self.registry["keys"].copy().items():
            if key_data["status"] != "active":
                continue

            if key_data["expiration_date"]:
                exp_date = datetime.fromisoformat(key_data["expiration_date"].replace("Z", "+00:00"))
                if now >= exp_date:
                    # Mark as expired
                    key_data["status"] = "expired"
                    key_data["updated_at"] = datetime.utcnow().isoformat() + "Z"
                    cleaned_keys.append(key_id)

        self._save_registry()
        return cleaned_keys

    def _save_registry(self):
        """Save the key registry to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.registry, f, indent=2)


# Example usage
if __name__ == "__main__":
    # Initialize the quantum key management system
    qkms = QuantumKeyManagementSystem()

    # Generate a quantum-safe key
    key_id = qkms.generate_quantum_key(
        security_level=QuantumSecurityLevel.QUANTUM_SAFE,
        algorithm="lattice-based-post-quantum"
    )
    print(f"Generated quantum-safe key with ID: {key_id}")

    # Retrieve and display key information
    key_info = qkms.get_key(key_id)
    print(f"Key info: {key_info}")

    # List all keys
    all_keys = qkms.list_keys()
    print(f"All keys: {len(all_keys)}")

    # Clean up any expired keys (there shouldn't be any yet)
    cleaned = qkms.cleanup_expired_keys()
    print(f"Cleaned up {len(cleaned)} expired keys")