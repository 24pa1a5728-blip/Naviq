import re

with open("main.py", "r") as f:
    content = f.read()

# Replace the exception block
new_except = """
        except Exception as e:
            error_msg = str(e)
            print(f"❌ FAILED TO SEND REAL SMS: {error_msg}")
            if "trial accounts" in error_msg.lower():
                raise HTTPException(status_code=400, detail="Twilio Trial Account Error: You must use your Twilio Virtual Phone Number as the sender (not your personal number), and you can only send to verified phone numbers.")
            else:
                raise HTTPException(status_code=400, detail=f"Twilio Error: {error_msg}")
"""

content = re.sub(r"except Exception as e:.*?raise HTTPException\(status_code=500, detail=\"Failed to send real SMS via Twilio\.\"\)", new_except.strip(), content, flags=re.DOTALL)

with open("main.py", "w") as f:
    f.write(content)
print("Patched exception block.")
