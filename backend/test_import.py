try:
    from main import app
    print("Main app imported successfully")
    print("App:", type(app))
except Exception as e:
    print(f"Error importing main app: {e}")
    import traceback
    traceback.print_exc()