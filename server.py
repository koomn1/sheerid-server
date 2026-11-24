from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app) # السماح بالاتصال من GitHub Pages

@app.route('/api/verify', methods=['POST'])
def verify():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"success": False, "error": "URL is missing"}), 400

    try:
        # هنا بنشغل الأداة (افترض إنها في نفس الفولدر)
        # غير المسار لو الأداة في فولدر تاني
        result = subprocess.run(
            ['python', 'SheerID-Verification-Tool/one-verify-tool/main.py', url],
            capture_output=True,
            text=True,
            timeout=120 # 2 دقيقة كحد أقصى
        )

        if result.returncode == 0:
            return jsonify({"success": True, "output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
