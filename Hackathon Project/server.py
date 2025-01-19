from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-python', methods=['POST'])
def run_python():
    data = request.get_json()
    code = data.get('code')

    try:
        # Save the Python code to a temporary file
        with open('temp_code.py', 'w') as f:
            f.write(code)

        # Run the Python code and capture the output
        result = subprocess.run(['python3', 'temp_code.py'], capture_output=True, text=True)

        # Send the result back as JSON
        return jsonify(output=result.stdout if result.returncode == 0 else result.stderr)

    except Exception as e:
        return jsonify(output=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)




