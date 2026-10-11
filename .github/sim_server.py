
import http.server, json, os, subprocess, sys, time, urllib.parse
KEY = os.environ["SIM_KEY"]; UDID = os.environ["UDID"]
def sh(cmd, timeout=100):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return {"rc": p.returncode, "out": p.stdout[-200000:], "err": p.stderr[-20000:]}
class H(http.server.BaseHTTPRequestHandler):
    def _ok(self):
        k = self.headers.get("X-Key") or urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("k", [""])[0]
        if k != KEY:
            self.send_response(403); self.end_headers(); return False
        return True
    def _json(self, obj, code=200):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if not self._ok(): return
        path = urllib.parse.urlparse(self.path).path
        try:
            if path == "/ping": return self._json({"ok": True, "udid": UDID, "t": time.time()})
            if path == "/shot":
                subprocess.run(f"xcrun simctl io {UDID} screenshot --type=png /tmp/shot.png", shell=True, capture_output=True, timeout=60)
                b = open("/tmp/shot.png","rb").read(); self.send_response(200); self.send_header("Content-Type","image/png"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
            if path == "/ui": return self._json(sh(f"axe describe-ui --udid {UDID}", 90))
            return self._json({"error": "unknown"}, 404)
        except Exception as e: return self._json({"error": repr(e)}, 500)
    def do_POST(self):
        if not self._ok(): return
        path = urllib.parse.urlparse(self.path).path
        n = int(self.headers.get("Content-Length") or 0); body = json.loads(self.rfile.read(n) or b"{}")
        try:
            if path == "/sh": return self._json(sh(body["cmd"], body.get("timeout", 100)))
            if path == "/tap": return self._json(sh(f"axe tap -x {body['x']} -y {body['y']} --udid {UDID}"))
            if path == "/swipe": return self._json(sh(f"axe swipe --start-x {body['x1']} --start-y {body['y1']} --end-x {body['x2']} --end-y {body['y2']} --duration {body.get('d',0.4)} --udid {UDID}"))
            if path == "/type":
                p = subprocess.run(["axe","type","--stdin","--udid",UDID], input=body["text"], capture_output=True, text=True, timeout=100)
                return self._json({"rc": p.returncode, "out": p.stdout[-2000:], "err": p.stderr[-2000:]})
            if path == "/quit":
                open("/tmp/quit","w").write("1"); return self._json({"ok": True})
            return self._json({"error": "unknown"}, 404)
        except Exception as e: return self._json({"error": repr(e)}, 500)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 8080), H).serve_forever()
