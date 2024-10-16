import http.server
import ssl
import os

PORT = 8000

cert_file = "cert.pem"
key_file = "key.pem"

# ファイルの存在を確認
if not os.path.exists(cert_file) or not os.path.exists(key_file):
    raise FileNotFoundError(f"Could not find cert.pem or key.pem in the directory: {os.getcwd()}")

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')  # ここでCORSを許可
        http.server.SimpleHTTPRequestHandler.end_headers(self)

httpd = http.server.HTTPServer(('localhost', PORT), CORSRequestHandler)

# TLSサーバーの設定
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=cert_file, keyfile=key_file)

# サーバーソケットをSSLでラップ
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving on https://localhost:{PORT}")
httpd.serve_forever()