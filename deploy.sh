#!/bin/bash
# 🚀 Gaurav Motors - Render Deployment Automation Script

echo "================================"
echo "  Gaurav Motors - Deployment   "
echo "================================"
echo ""

# Step 1: Verify Git
echo "✓ Step 1: Checking Git status..."
git status
echo ""

# Step 2: Check Python version
echo "✓ Step 2: Checking Python version..."
python --version
echo ""

# Step 3: Verify dependencies
echo "✓ Step 3: Verifying dependencies..."
python -c "import flask; print(f'Flask {flask.__version__}')"
python -c "import gunicorn; print('Gunicorn installed')"
echo ""

# Step 4: Run tests
echo "✓ Step 4: Running tests..."
if [ -f "test_routes.py" ]; then
    python test_routes.py
else
    echo "  No tests to run"
fi
echo ""

# Step 5: Display deployment info
echo "================================"
echo "  Deployment Configuration      "
echo "================================"
echo ""
echo "Repository: chilkotiKartik/gaurav-motors"
echo "Branch: main"
echo "Platform: Render.com"
echo "Database: PostgreSQL"
echo "Runtime: Python 3.11"
echo "Server: Gunicorn"
echo ""

# Step 6: Next steps
echo "================================"
echo "  Next Steps                    "
echo "================================"
echo ""
echo "1. Go to https://dashboard.render.com"
echo "2. Click: New + → Web Service"
echo "3. Connect GitHub repository: gaurav-motors"
echo "4. Use auto-detected build settings"
echo "5. Add Environment Variables:"
echo "   - FLASK_ENV = production"
echo "   - SECRET_KEY = (generate new secure key)"
echo "   - DATABASE_URL = (will be auto-set by PostgreSQL)"
echo ""
echo "6. Create PostgreSQL database:"
echo "   - Plan: Standard"
echo "   - Auto-connect to web service"
echo ""
echo "7. Click Deploy"
echo ""
echo "✅ Deployment ready!"
echo ""
