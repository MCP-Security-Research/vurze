/* Use SHA-256 to sign functions and classes in a python file. */

use sha2::{Sha256, Digest};

/// Generate a SHA-256 hash from input data
pub fn generate_hash(data: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    let result = hasher.finalize();
    format!("{:x}", result)
}

/// Verify if a hash matches the input data
pub fn verify_hash(hash: &str, data: &str) -> bool {
    let computed_hash = generate_hash(data);
    computed_hash == hash.to_lowercase()
}
