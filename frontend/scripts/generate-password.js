/**
 * Helper script to generate bcrypt password hashes for user creation
 * Usage: node scripts/generate-password.js <password>
 * Example: node scripts/generate-password.js admin123
 */

const bcrypt = require('bcryptjs');

const password = process.argv[2];

if (!password) {
  console.error('Error: Please provide a password as argument');
  console.log('Usage: node scripts/generate-password.js <password>');
  process.exit(1);
}

const hash = bcrypt.hashSync(password, 10);

console.log('\n=== Password Hash Generated ===\n');
console.log('Password:', password);
console.log('Hash:', hash);
console.log('\nUse this SQL to create a user:\n');
console.log(`INSERT INTO users (username, email, password_hash, role, is_active)`);
console.log(`VALUES ('your_username', 'your@email.com', '${hash}', 'admin', true);`);
console.log('');
