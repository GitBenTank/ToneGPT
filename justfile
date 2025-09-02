# ToneGPT Development Commands
# Convenient shortcuts for testing, auditing, and linting

# Run all tests
test:
    python -m pytest tests/ -v

# Run FM9 parameter audit
audit:
    python fm9_param_audit.py \
        --blocks tonegpt/core/blocks_with_footswitch.json \
        --cfg data/fm9_config.json \
        --ref data/fm9_comprehensive_reference.json \
        --out report/fm9_param_audit.md

# Run linting (black formatting)
lint:
    black tonegpt/ tests/ fm9_param_audit.py

# Build blocks_featured.json
build-blocks:
    python tools/build_blocks_featured.py

# Run all checks (test + audit + lint)
check: test audit lint

# Run specific test suites
test-golden:
    python -m pytest tests/test_golden_presets.py -v

test-negative:
    python -m pytest tests/test_negative_cases.py -v

test-audit:
    python -m pytest tests/test_param_audit.py -v

test-spec:
    python -m pytest tests/spec_fm9_mapping.py -v

# Run Streamlit app
run:
    streamlit run ui/frontend_ai_v4.py --server.port 8504

# Clean up generated files
clean:
    rm -rf report/
    rm -rf tests/data/golden_presets/*.json
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Show help
help:
    @echo "ToneGPT Development Commands:"
    @echo "  just test       - Run all tests"
    @echo "  just audit      - Run FM9 parameter audit"
    @echo "  just lint       - Run black + mypy linting"
    @echo "  just build-blocks - Build blocks_featured.json"
    @echo "  just check      - Run all checks (test + audit + lint)"
    @echo "  just run        - Run Streamlit app"
    @echo "  just clean      - Clean up generated files"
    @echo "  just help       - Show this help"
    @echo ""
    @echo "Specific test suites:"
    @echo "  just test-golden  - Run golden preset tests"
    @echo "  just test-negative - Run negative case tests"
    @echo "  just test-audit   - Run parameter audit tests"
    @echo "  just test-spec    - Run FM9 mapping spec tests"
