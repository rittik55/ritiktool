import sys
import os

tool_dir = os.path.join(os.path.dirname(__file__), "ritiktool")
sys.path.insert(0, tool_dir)

if __name__ == "__main__":
    import mitool
    mitool.main()
