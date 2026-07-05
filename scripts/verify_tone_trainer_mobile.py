#!/usr/bin/env python3
import json
import os
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


LONG_SENTENCE = {
    "id": "mobile-long-001",
    "unitId": "default",
    "zh": "我今天下午想跟我的中国朋友一起练习很长很长的普通话声调句子",
    "spokenZh": "我今天下午想跟我的中国朋友一起练习很长很长的普通话声调句子",
    "en": "This intentionally long sentence should wrap cleanly on phones.",
    "syl": [
        {"p": "wo3", "t": 3},
        {"p": "jin1", "t": 1},
        {"p": "tian1", "t": 1},
        {"p": "xia4", "t": 4},
        {"p": "wu3", "t": 3},
        {"p": "xiang3", "t": 3},
        {"p": "gen1", "t": 1},
        {"p": "wo3", "t": 3},
        {"p": "de", "t": 0, "s": "weak"},
        {"p": "zhong1", "t": 1},
        {"p": "guo2", "t": 2},
        {"p": "peng2", "t": 2},
        {"p": "you3", "t": 3},
        {"p": "yi4", "t": 4},
        {"p": "qi3", "t": 3},
        {"p": "lian4", "t": 4},
        {"p": "xi2", "t": 2},
        {"p": "hen3", "t": 3},
        {"p": "chang2", "t": 2},
        {"p": "hen3", "t": 3},
        {"p": "chang2", "t": 2},
        {"p": "de", "t": 0, "s": "weak"},
        {"p": "pu3", "t": 3},
        {"p": "tong1", "t": 1},
        {"p": "hua4", "t": 4},
        {"p": "sheng1", "t": 1},
        {"p": "diao4", "t": 4},
        {"p": "ju4", "t": 4},
        {"p": "zi", "t": 0, "s": "weak"},
    ],
}

SHORT_SENTENCE = {
    "id": "mobile-short-001",
    "unitId": "default",
    "zh": "你好",
    "spokenZh": "你好",
    "en": "Hello.",
    "syl": [{"p": "ni3", "t": 3}, {"p": "hao3", "t": 3}],
}

LOGIN_PAYLOAD = {
    "label": "MOBILE TEST",
    "decks": [
        {
            "id": "mobile",
            "name": "Mobile Long Sentences",
            "full": True,
            "units": [{"id": "default", "name": "全部"}],
            "sents": [LONG_SENTENCE, SHORT_SENTENCE],
        }
    ],
    "audio": {
        "mobile-long-001": {
            "f": {
                "n": "/fake-audio/mobile-long-normal.mp3",
                "s": "/fake-audio/mobile-long-slow.mp3",
            }
        },
        "mobile-short-001": {
            "f": {
                "n": "/fake-audio/mobile-short-normal.mp3",
                "s": "/fake-audio/mobile-short-slow.mp3",
            }
        },
    },
}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def log_message(self, fmt, *args):
        return

    def do_POST(self):
        if self.path == "/api/login":
            body = json.dumps(LOGIN_PAYLOAD, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_error(404)

    def do_GET(self):
        if self.path.startswith("/fake-audio/"):
            body = b"fake"
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def assert_no_horizontal_overflow(page, width):
    offenders = page.evaluate(
        """
        () => {
          const doc = document.documentElement;
          const maxWidth = doc.clientWidth + 1;
          return [...document.querySelectorAll('body, #app, .stage, .sentence .zh, .sentence .py, #toneGrid, .tone-cell, .list-panel, .item, .item .zh, .item .py')]
            .map(el => {
              const rect = el.getBoundingClientRect();
              return {
                selector: el === document.body ? 'body' : (
                  el.id ? `#${el.id}` : (
                    el.className ? `.${String(el.className).trim().replace(/\\s+/g,'.')}` : el.tagName
                  )
                ),
                left: Math.floor(rect.left),
                right: Math.ceil(rect.right),
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth,
                text: (el.textContent || '').trim().slice(0, 40)
              };
            })
            .filter(item => item.right > maxWidth || item.left < -1 || item.scrollWidth > item.clientWidth + 1);
        }
        """
    )
    assert offenders == [], f"{width}px overflow offenders: {offenders}"


def login(page, base_url, code="mobile-test-code"):
    page.goto(f"{base_url}/tone_trainer-ponk.html", wait_until="domcontentloaded")
    page.fill("#pw", code)
    page.click("#enter")
    page.wait_for_selector("#app", state="visible")
    page.wait_for_timeout(350)


def install_browser_mocks(page):
    page.add_init_script(
        """
        (() => {
          class FakeAudio {
            constructor(src) {
              this.src = src;
              this.duration = 2.4;
              this.currentTime = 0;
              this._events = {};
            }
            addEventListener(name, fn) { this._events[name] = fn; }
            play() {
              setTimeout(() => this._events.loadedmetadata && this._events.loadedmetadata(), 0);
              return Promise.resolve();
            }
            pause() {}
            load() {}
          }
          window.Audio = FakeAudio;
          window.speechSynthesis = {
            getVoices: () => [],
            cancel: () => {},
            speak: () => {}
          };
          class FakeRecorder {
            constructor(stream, options = {}) {
              this.stream = stream;
              this.mimeType = options.mimeType || 'audio/webm';
              this.state = 'inactive';
              this._events = {};
            }
            static isTypeSupported() { return true; }
            addEventListener(name, fn) { this._events[name] = fn; }
            start() { this.state = 'recording'; }
            stop() {
              this.state = 'inactive';
              const blob = new Blob(['tone'], { type: this.mimeType });
              this._events.dataavailable && this._events.dataavailable({ data: blob });
              this._events.stop && this._events.stop();
            }
          }
          window.MediaRecorder = FakeRecorder;
          Object.defineProperty(navigator, 'mediaDevices', {
            value: {
              getUserMedia: () => Promise.resolve({
                getTracks: () => [{ stop: () => {} }]
              })
            },
            configurable: true
          });
        })();
        """
    )


def verify_width(browser, base_url, width):
    context = browser.new_context(viewport={"width": width, "height": 900}, is_mobile=width < 600)
    page = context.new_page()
    install_browser_mocks(page)
    login(page, base_url)

    assert_no_horizontal_overflow(page, width)

    page.click("#play")
    page.wait_for_selector(".tone-cell.active")

    page.click("#recStart")
    page.wait_for_selector("#recStop:not([disabled])")
    page.click("#recStop")
    page.wait_for_selector("#recPlay:not([disabled])")
    page.click("#recPlay")

    page.click("#markHard")
    page.wait_for_selector("#hardList .item")
    hard_text = page.locator("#hardList").inner_text()
    assert LONG_SENTENCE["zh"] in hard_text
    assert page.locator("#practiceMeta").inner_text().find("1") != -1

    page.click("#next")
    page.click("#hardList .item")
    assert page.locator("#sZh").inner_text() == LONG_SENTENCE["zh"]

    page.click("#markHard")
    page.wait_for_selector("#hardList .empty-state")
    assert "0" in page.locator("#hardMeta").inner_text()

    assert_no_horizontal_overflow(page, width)
    context.close()


def verify_access_code_isolation(browser, base_url):
    context = browser.new_context(viewport={"width": 390, "height": 900}, is_mobile=True)
    page = context.new_page()
    install_browser_mocks(page)

    login(page, base_url, "student-a")
    page.click("#play")
    page.wait_for_selector(".tone-cell.active")
    page.click("#markHard")
    page.wait_for_selector("#hardList .item")
    assert LONG_SENTENCE["zh"] in page.locator("#hardList").inner_text()
    assert "1" in page.locator("#practiceMeta").inner_text()

    page.goto("about:blank")
    login(page, base_url, "student-b")
    page.wait_for_selector("#hardList .empty-state")
    assert "0" in page.locator("#practiceMeta").inner_text()
    assert LONG_SENTENCE["zh"] not in page.locator("#hardList").inner_text()

    page.goto("about:blank")
    login(page, base_url, "student-a")
    page.wait_for_selector("#hardList .item")
    assert LONG_SENTENCE["zh"] in page.locator("#hardList").inner_text()
    assert "1" in page.locator("#practiceMeta").inner_text()

    context.close()


def main():
    os.chdir(ROOT)
    server = start_server()
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                for width in (390, 430, 768):
                    verify_width(browser, base_url, width)
                verify_access_code_isolation(browser, base_url)
            finally:
                browser.close()
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
