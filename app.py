from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = 8001


def get_page():
    return """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <title>Calculator</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #dfe9f3, #f5f7fa);
      font-family: Arial, sans-serif;
    }
    .calculator {
      width: 340px;
      background: #1f1f2e;
      border-radius: 22px;
      padding: 22px 18px 18px;
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);
    }
    .display {
      height: 90px;
      background: #e8f0f7;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding: 0 18px;
      margin-bottom: 18px;
      font-size: 2rem;
      font-weight: 700;
      color: #1d2333;
      overflow: hidden;
      word-break: break-all;
    }
    .buttons {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }
    button {
      border: none;
      border-radius: 14px;
      font-size: 1.2rem;
      font-weight: 700;
      height: 58px;
      cursor: pointer;
      transition: transform 0.08s ease, filter 0.15s ease;
    }
    button:hover { filter: brightness(1.08); }
    button:active { transform: scale(0.98); }
    .operator {
      background: #ffb74d;
      color: #1d2333;
    }
    .action {
      background: #8dc5ff;
      color: #0b1d33;
    }
    .digit {
      background: #f3f5f7;
      color: #1d2333;
    }
    .zero {
      grid-column: span 2;
    }
    .equals {
      background: #5ac77b;
      color: white;
    }
  </style>
</head>
<body>
  <div class='calculator'>
    <div id='display' class='display'>0</div>
    <div class='buttons'>
      <button class='action' data-action='clear'>C</button>
      <button class='action' data-action='toggle'>±</button>
      <button class='action' data-action='percent'>%</button>
      <button class='operator' data-action='divide'>÷</button>

      <button class='digit' data-value='7'>7</button>
      <button class='digit' data-value='8'>8</button>
      <button class='digit' data-value='9'>9</button>
      <button class='operator' data-action='multiply'>×</button>

      <button class='digit' data-value='4'>4</button>
      <button class='digit' data-value='5'>5</button>
      <button class='digit' data-value='6'>6</button>
      <button class='operator' data-action='subtract'>−</button>

      <button class='digit' data-value='1'>1</button>
      <button class='digit' data-value='2'>2</button>
      <button class='digit' data-value='3'>3</button>
      <button class='operator' data-action='add'>+</button>

      <button class='digit zero' data-value='0'>0</button>
      <button class='digit' data-value='.'>.</button>
      <button class='equals' data-action='equals'>=</button>
    </div>
  </div>

  <script>
    const display = document.getElementById('display');
    let currentValue = '0';
    let storedValue = null;
    let pendingOp = null;
    let justEvaluated = false;

    function updateDisplay() {
      display.textContent = currentValue;
    }

    function clearAll() {
      currentValue = '0';
      storedValue = null;
      pendingOp = null;
      justEvaluated = false;
      updateDisplay();
    }

    function appendDigit(value) {
      if (justEvaluated) {
        currentValue = '0';
        justEvaluated = false;
      }
      if (value === '.' && currentValue.includes('.')) {
        return;
      }
      currentValue = currentValue === '0' && value !== '.' ? value : currentValue + value;
      updateDisplay();
    }

    function applyPercent() {
      const value = Number(currentValue) / 100;
      currentValue = String(value);
      updateDisplay();
    }

    function toggleSign() {
      const value = Number(currentValue);
      currentValue = String(-value);
      updateDisplay();
    }

    function doCalculation() {
      const current = Number(currentValue);
      if (storedValue === null || pendingOp === null) {
        return;
      }
      let result = 0;
      switch (pendingOp) {
        case 'add':
          result = storedValue + current;
          break;
        case 'subtract':
          result = storedValue - current;
          break;
        case 'multiply':
          result = storedValue * current;
          break;
        case 'divide':
          if (current === 0) {
            currentValue = 'Error';
            storedValue = null;
            pendingOp = null;
            justEvaluated = true;
            updateDisplay();
            return;
          }
          result = storedValue / current;
          break;
        default:
          return;
      }
      currentValue = String(result);
      storedValue = null;
      pendingOp = null;
      justEvaluated = true;
      updateDisplay();
    }

    function setOperation(op) {
      if (pendingOp !== null && storedValue !== null && !justEvaluated) {
        doCalculation();
      }
      storedValue = Number(currentValue);
      pendingOp = op;
      justEvaluated = false;
      currentValue = '0';
      updateDisplay();
    }

    document.querySelectorAll('.digit').forEach((button) => {
      button.addEventListener('click', () => appendDigit(button.dataset.value));
    });

    document.querySelectorAll('.operator').forEach((button) => {
      button.addEventListener('click', () => setOperation(button.dataset.action));
    });

    document.querySelector('[data-action="clear"]').addEventListener('click', clearAll);
    document.querySelector('[data-action="toggle"]').addEventListener('click', toggleSign);
    document.querySelector('[data-action="percent"]').addEventListener('click', applyPercent);
    document.querySelector('[data-action="equals"]').addEventListener('click', doCalculation);
  </script>
</body>
</html>"""


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(get_page().encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), CalculatorHandler)
    print(f"Calculator app running at http://localhost:{PORT}")
    server.serve_forever()
