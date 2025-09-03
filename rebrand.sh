#!/bin/bash
# ToneGPT Rebranding Script
# Usage: ./rebrand.sh "New Brand Name" "new@email.com"

if [ $# -ne 2 ]; then
    echo "Usage: $0 \"New Brand Name\" \"new@email.com\""
    echo "Example: $0 \"ToneForge AI\" \"ben@toneforge.com\""
    exit 1
fi

NEW_NAME="$1"
NEW_EMAIL="$2"
OLD_NAME="ToneGPT"
OLD_EMAIL="ben@tonegpt.com"

echo "🔄 Starting rebranding process..."
echo "Old: $OLD_NAME ($OLD_EMAIL)"
echo "New: $NEW_NAME ($NEW_EMAIL)"
echo ""

# Update Python files
echo "📝 Updating Python files..."
find . -type f -name "*.py" -exec sed -i.bak "s/$OLD_NAME/$NEW_NAME/g" {} \;
find . -type f -name "*.py" -exec sed -i.bak "s/$OLD_EMAIL/$NEW_EMAIL/g" {} \;

# Update Markdown files
echo "📝 Updating Markdown files..."
find . -type f -name "*.md" -exec sed -i.bak "s/$OLD_NAME/$NEW_NAME/g" {} \;
find . -type f -name "*.md" -exec sed -i.bak "s/$OLD_EMAIL/$NEW_EMAIL/g" {} \;

# Update JSON files
echo "📝 Updating JSON files..."
find . -type f -name "*.json" -exec sed -i.bak "s/$OLD_NAME/$NEW_NAME/g" {} \;

# Update README badge
echo "📝 Updating README badge..."
sed -i.bak "s/ToneGPT AI/$NEW_NAME/g" README.md

# Clean up backup files
echo "🧹 Cleaning up backup files..."
find . -name "*.bak" -delete

echo ""
echo "✅ Rebranding complete!"
echo "📋 Next steps:"
echo "   1. Update domain and hosting"
echo "   2. Design new logo and branding"
echo "   3. Update social media accounts"
echo "   4. Test all functionality"
echo "   5. Commit changes to git"
echo ""
echo "🎸 $NEW_NAME is ready to rock!"
