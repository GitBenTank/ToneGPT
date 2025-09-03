#!/bin/bash
# Setup Public Repository Script
# This script prepares your code for public GitHub while protecting business docs

echo "🔒 Setting up public repository structure..."

# Create backup of current state
echo "📦 Creating backup..."
cp -r . ../ToneGPT-backup-$(date +%Y%m%d-%H%M%S)

# Move business docs to private location
echo "🔐 Moving business documents to private location..."
mkdir -p ../ToneGPT-Private-Business
mv FM9_ACQUISITION_PACKAGE.md ../ToneGPT-Private-Business/
mv REBRANDING_SYSTEM.md ../ToneGPT-Private-Business/
mv FM9_DEMO_SCRIPT.md ../ToneGPT-Private-Business/
mv rebrand.sh ../ToneGPT-Private-Business/

# Setup public repository
echo "🌐 Setting up public repository..."
cp README_PUBLIC.md README.md
cp .gitignore_public .gitignore

# Remove any remaining private files
echo "🧹 Cleaning up private files..."
rm -f *.personal
rm -f *.private
rm -f *.confidential
rm -f business_plan.*
rm -f acquisition_notes.*
rm -f demo_notes.*

# Create public repository structure
echo "📁 Creating public repository structure..."
mkdir -p docs/public
mkdir -p examples
mkdir -p screenshots

# Move public documentation
echo "📚 Organizing public documentation..."
cp TONEGPT_SYSTEM_OVERVIEW.md docs/public/
cp TONEGPT_PRODUCTION_SCHEMA.md docs/public/

# Create example queries file
echo "📝 Creating example queries..."
cat > examples/example_queries.txt << 'EOF'
# ToneGPT AI - Example Queries

## Basic Amp Tones
- "Marshall Plexi"
- "Fender Twin Reverb"
- "Mesa Boogie Rectifier"
- "Vox AC30"

## With Effects
- "Marshall Plexi with Tube Screamer"
- "Fender Twin with reverb and delay"
- "Mesa Rectifier with chorus"

## Genre-Specific
- "SRV-style blues"
- "Modern metal"
- "Clean jazz"
- "Country twang"

## Complex Combinations
- "Marshall Plexi with Tube Screamer and reverb"
- "Fender Twin with chorus, delay, and reverb"
- "Mesa Rectifier with overdrive and delay"
EOF

# Create screenshots directory with placeholder
echo "📸 Setting up screenshots directory..."
cat > screenshots/README.md << 'EOF'
# Screenshots

This directory contains screenshots of ToneGPT AI in action.

## Main Interface
- Main UI showing tone generation
- Block editors with parameter controls
- System statistics display

## Example Results
- Generated tone patches
- Parameter adjustments
- Real-time updates

*Screenshots will be added to showcase the application's capabilities.*
EOF

# Update git for public repository
echo "🔄 Updating git for public repository..."
git add .
git commit -m "🌐 PUBLIC REPOSITORY: Prepare for public GitHub release

- Move business strategy docs to private location
- Create public-facing README and documentation
- Add example queries and screenshots structure
- Maintain proprietary licensing protection
- Ready for public GitHub repository"

echo ""
echo "✅ Public repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create new GitHub repository (public)"
echo "2. Push this code to the public repository"
echo "3. Keep business docs in private location: ../ToneGPT-Private-Business/"
echo "4. Update any hardcoded URLs in the code"
echo ""
echo "🔒 Business documents are safely stored in:"
echo "   ../ToneGPT-Private-Business/"
echo ""
echo "🌐 Public code is ready for GitHub!"
echo ""
echo "💡 To restore business docs later:"
echo "   cp ../ToneGPT-Private-Business/* ."
