#!/bin/bash
# Safe Release Update Script
# Updates GitHub repository for safe, donation-based release

echo "🛡️ Updating repository for safe release..."

# Backup current files
echo "📦 Creating backup..."
cp README.md README_BACKUP.md
cp LICENSE LICENSE_BACKUP

# Update to safe versions
echo "🔄 Updating to safe versions..."
cp README_SAFE.md README.md
cp LICENSE_SAFE LICENSE

# Update any FM9-specific references to be more generic
echo "🔧 Updating references to be more generic..."

# Update the main README to remove FM9-specific claims
sed -i.bak 's/FM9 hardware/guitar hardware/g' README.md
sed -i.bak 's/FM9 patches/tone configurations/g' README.md
sed -i.bak 's/FM9-Edit software/audio software/g' README.md
sed -i.bak 's/FM9 integration/audio system integration/g' README.md

# Clean up backup files
rm -f README.md.bak

echo ""
echo "✅ Safe release update complete!"
echo ""
echo "📋 Changes made:"
echo "   - Updated README to research/donation-ware positioning"
echo "   - Changed license to MIT for open research"
echo "   - Removed FM9-specific claims"
echo "   - Added research disclaimers"
echo "   - Positioned as experimental project"
echo ""
echo "🚀 Ready to commit and push to GitHub!"
echo ""
echo "💡 Next steps:"
echo "   1. Review the changes"
echo "   2. Commit: git add . && git commit -m 'Safe release: Research project positioning'"
echo "   3. Push: git push origin main"
echo "   4. Create new release with safe messaging"
