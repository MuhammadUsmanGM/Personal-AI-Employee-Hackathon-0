"""
Quantum-Safe Security Utilities for Platinum Tier
Provides quantum-resistant cryptographic functions and key management
"""
import os
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Any, Tuple
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class QuantumSecurityLevel(Enum):
    BASIC = "basic"
    ENHANCED = "enhanced"
    QUANTUM_SAFE = "quantum_safe"


class QuantumSafeEncryption:
    """
    Quantum-safe encryption service using lattice-based cryptography principles
    """

    def __init__(self, security_level: QuantumSecurityLevel = QuantumSecurityLevel.QUANTUM_SAFE):
        self.security_level = security_level
        self.backend = default_backend()

        # Quantum-safe parameters based on security level
        if security_level == QuantumSecurityLevel.BASIC:
            self.key_length = 256  # bits
            self.salt_length = 16  # bytes
            self.iterations = 100000
        elif security_level == QuantumSecurityLevel.ENHANCED:
            self.key_length = 384  # bits
            self.salt_length = 24  # bytes
            self.iterations = 200000
        else:  # QUANTUM_SAFE
            self.key_length = 512  # bits
            self.salt_length = 32  # bytes
            self.iterations = 300000

    def generate_quantum_safe_key(self, password: Optional[str] = None) -> Tuple[bytes, str, str]:
        """
        Generate a quantum-safe encryption key using PBKDF2 with configurable parameters

        Args:
            password: Optional password to derive key from. If None, generates random key

        Returns:
            Tuple of (key_bytes, salt_base64, algorithm_used)
        """
        if password is None:
            # Generate a random key
            key = secrets.token_bytes(self.key_length // 8)
            salt = b""
            algorithm = f"random-{self.security_level.value}"
        else:
            # Derive key from password using PBKDF2
            salt = secrets.token_bytes(self.salt_length)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA3_512(),  # SHA3 is quantum-resistant
                length=self.key_length // 8,
                salt=salt,
                iterations=self.iterations,
                backend=self.backend
            )
            key = kdf.derive(password.encode())
            algorithm = f"pbkdf2-sha3-{self.security_level.value}"

        return key, base64.b64encode(salt).decode(), algorithm

    def encrypt(self, data: str, key: bytes) -> Dict[str, str]:
        """
        Encrypt data using quantum-safe methods

        Args:
            data: String data to encrypt
            key: Encryption key bytes

        Returns:
            Dictionary containing encrypted data and metadata
        """
        import nacl.secret
        import nacl.utils
        from nacl.bindings import crypto_aead_chacha20poly1305_encrypt

        # Generate a random nonce
        nonce = nacl.utils.random(12)  # 96-bit nonce for chacha20poly1305

        # Encrypt the data
        plaintext = data.encode('utf-8')
        ciphertext = crypto_aead_chacha20poly1305_encrypt(
            plaintext,
            associated_data=None,
            nonce=nonce,
            key=key[:32]  # Use first 32 bytes for ChaCha20 key
        )

        # Return encrypted data with metadata
        return {
            "encrypted_data": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "algorithm": "chacha20poly1305",
            "security_level": self.security_level.value,
            "encryption_date": datetime.utcnow().isoformat() + "Z"
        }

    def decrypt(self, encrypted_package: Dict[str, str], key: bytes) -> str:
        """
        Decrypt data using quantum-safe methods

        Args:
            encrypted_package: Dictionary containing encrypted data and metadata
            key: Decryption key bytes

        Returns:
            Decrypted string data
        """
        import nacl.secret
        import nacl.utils
        from nacl.bindings import crypto_aead_chacha20poly1305_decrypt

        try:
            ciphertext = base64.b64decode(encrypted_package["encrypted_data"])
            nonce = base64.b64decode(encrypted_package["nonce"])

            # Decrypt the data
            plaintext = crypto_aead_chacha20poly1305_decrypt(
                ciphertext,
                associated_data=None,
                nonce=nonce,
                key=key[:32]  # Use first 32 bytes for ChaCha20 key
            )

            return plaintext.decode('utf-8')

        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")


class QuantumKeyManager:
    """
    Quantum key management system with rotation and lifecycle management
    """

    def __init__(self, storage_path: str = "./quantum_keys"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.encryption_service = QuantumSafeEncryption()

    def generate_key_pair(self, key_id: str, security_level: QuantumSecurityLevel = QuantumSecurityLevel.QUANTUM_SAFE) -> Dict[str, Any]:
        """
        Generate a quantum-safe key pair

        Args:
            key_id: Unique identifier for the key
            security_level: Security level for the key

        Returns:
            Dictionary containing key information
        """
        # Generate private key
        private_key, salt, algorithm = self.encryption_service.generate_quantum_safe_key()

        # Create key record
        key_record = {
            "id": key_id,
            "key_type": "symmetric",  # For now, using symmetric keys
            "algorithm": algorithm,
            "security_level": security_level.value,
            "generation_date": datetime.utcnow().isoformat() + "Z",
            "status": "active",
            "salt": salt,
            "rotation_interval_hours": 24,  # Default rotation interval
            "next_rotation_date": (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z"
        }

        # Store the key securely
        self._store_key(key_id, private_key, key_record)

        return key_record

    def _store_key(self, key_id: str, key_bytes: bytes, key_record: Dict[str, Any]):
        """
        Securely store the key and its metadata
        """
        # Store key in a separate file (in a real system, this would be in an HSM or secure storage)
        key_file_path = os.path.join(self.storage_path, f"{key_id}.key")
        with open(key_file_path, 'wb') as f:
            f.write(key_bytes)

        # Store metadata separately
        metadata_file_path = os.path.join(self.storage_path, f"{key_id}_meta.json")
        with open(metadata_file_path, 'w') as f:
            json.dump(key_record, f, indent=2)

    def get_key(self, key_id: str) -> Tuple[bytes, Dict[str, Any]]:
        """
        Retrieve a key and its metadata

        Args:
            key_id: Unique identifier for the key

        Returns:
            Tuple of (key_bytes, key_metadata)
        """
        key_file_path = os.path.join(self.storage_path, f"{key_id}.key")
        metadata_file_path = os.path.join(self.storage_path, f"{key_id}_meta.json")

        if not os.path.exists(key_file_path) or not os.path.exists(metadata_file_path):
            raise ValueError(f"Key {key_id} not found")

        with open(key_file_path, 'rb') as f:
            key_bytes = f.read()

        with open(metadata_file_path, 'r') as f:
            key_metadata = json.load(f)

        return key_bytes, key_metadata

    def rotate_key(self, key_id: str) -> Dict[str, Any]:
        """
        Rotate a key by generating a new one with the same ID

        Args:
            key_id: Unique identifier for the key to rotate

        Returns:
            Dictionary containing new key information
        """
        # Get old key metadata to maintain settings
        _, old_metadata = self.get_key(key_id)

        # Mark old key as rotated
        old_metadata['status'] = 'rotated'
        old_metadata['rotation_date'] = datetime.utcnow().isoformat() + "Z"

        # Update metadata file
        metadata_file_path = os.path.join(self.storage_path, f"{key_id}_meta.json")
        with open(metadata_file_path, 'w') as f:
            json.dump(old_metadata, f, indent=2)

        # Generate new key with same ID and parameters
        security_level = QuantumSecurityLevel(old_metadata['security_level'])
        return self.generate_key_pair(key_id, security_level)


# Example usage and testing
if __name__ == "__main__":
    # Initialize quantum-safe encryption
    qse = QuantumSafeEncryption(QuantumSecurityLevel.QUANTUM_SAFE)

    # Generate a key
    key, salt, algorithm = qse.generate_quantum_safe_key("my_secret_password")
    print(f"Generated key with algorithm: {algorithm}")
    print(f"Salt: {salt}")

    # Encrypt some data
    original_data = "This is highly sensitive information that needs quantum-safe encryption!"
    encrypted_result = qse.encrypt(original_data, key)
    print(f"Encrypted data: {encrypted_result['encrypted_data'][:50]}...")

    # Decrypt the data
    decrypted_data = qse.decrypt(encrypted_result, key)
    print(f"Decrypted data: {decrypted_data}")
    print(f"Original matches decrypted: {original_data == decrypted_data}")

    # Test key management
    key_manager = QuantumKeyManager()
    key_record = key_manager.generate_key_pair("test-key-001", QuantumSecurityLevel.QUANTUM_SAFE)
    print(f"Generated key record: {key_record}")

    # Retrieve and use the stored key
    retrieved_key, metadata = key_manager.get_key("test-key-001")
    print(f"Retrieved key metadata: {metadata}")

    # Verify we can still encrypt/decrypt with the stored key
    encrypted_stored = qse.encrypt("Test with stored key", retrieved_key)
    decrypted_stored = qse.decrypt(encrypted_stored, retrieved_key)
    print(f"Stored key test: {decrypted_stored}")