from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

HOST = "0.0.0.0"
PORT = 8001


def calculate(num1, num2, operation):
    if operation == "add":
        return num1 + num2
    if operation == "subtract":
        return num1 - num2
    if operation == "multiply":
        return num1 * num2
    if operation == "divide":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return num1 / num2
    raise ValueError("Invalid operation selected.")


def get_page(result=None, error=None):
    result_html = ""
    if result is not None:
        result_html = f"<div class='result-box'><h2>Result</h2><p>{result}</p></div>"

    error_html = ""
    if error:
        error_html = f"<p class='error'>{error}</p>"

    return f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <title>Calculator</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #e0f7fa, #f5f5f5);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }}
    .container {{
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
      padding: 30px;
      width: 360px;
    }}
    h1 {{ text-align: center; margin-bottom: 24px; }}
    .input-row {{ display: flex; flex-direction: column; margin-bottom: 16px; }}
    label {{ margin-bottom: 6px; font-weight: bold; }}
    input, select, button {{ padding: 10px 12px; font-size: 1rem; border-radius: 8px; border: 1px solid #ccc; }}
    button {{ width: 100%; background: #007bff; color: white; border: none; cursor: pointer; margin-top: 8px; }}
    button:hover {{ background: #0056b3; }}
    .result-box {{ margin-top: 24px; background: #f8f9fa; border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; text-align: center; }}
    .error {{ color: #b00020; margin-top: 16px; text-align: center; font-weight: bold; }}
  </style>
</head>
<body>
  <div class='container'>
    <h1>Basic Calculator</h1>
    <form method='POST'>
      <div class='input-row'>
        <label for='num1'>Number 1</label>
        <input type='number' step='any' name='num1' required />
      </div>
      <div class='input-row'>
        <label for='operation'>Operation</label>
        <select name='operation'>
          <option value='add'>Addition (+)</option>
          <option value='subtract'>Subtraction (-)</option>
          <option value='multiply'>Multiplication (×)</option>
          <option value='divide'>Division (÷)</option>
        </select>
      </div>
      <div class='input-row'>
        <label for='num2'>Number 2</label>
        <input type='number' step='any' name='num2' required />
      </div>
      <button type='submit'>Calculate</button>
    </form>
    {error_html}
    {result_html}
  </div>
</body>
</html>"""


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(get_page().encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        data = parse_qs(raw.decode("utf-8"))

        try:
            num1 = float(data.get("num1", ["0"])[0])
            num2 = float(data.get("num2", ["0"])[0])
            operation = data.get("operation", ["add"])[0]
            result = calculate(num1, num2, operation)
            error = None
        except ZeroDivisionError:
            result = None
            error = "Cannot divide by zero."
        except ValueError:
            result = None
            error = "Please enter valid numbers."
        except Exception:
            result = None
            error = "Invalid operation selected."

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(get_page(result=result, error=error).encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), CalculatorHandler)
    print(f"Calculator app running at http://localhost:{PORT}")
    server.serve_forever()
