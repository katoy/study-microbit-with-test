import os
import re
import time
import pytest
from playwright.sync_api import sync_playwright

EXPECTED_DIRECTIONS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

EXPECTED_PATTERNS = [
    # 0° (北 N - NORTH)
    "\n".join([
        "..#..",
        ".###.",
        "#.#.#",
        "..#..",
        "..#.."
    ]),
    # 45° (北東 NE - NORTH_EAST)
    "\n".join([
        "..###",
        "...##",
        "..#.#",
        ".#...",
        "#...."
    ]),
    # 90° (東 E - EAST)
    "\n".join([
        "..#..",
        "...#.",
        "#####",
        "...#.",
        "..#.."
    ]),
    # 135° (南東 SE - SOUTH_EAST)
    "\n".join([
        "#....",
        ".#...",
        "..#.#",
        "...##",
        "..###"
    ]),
    # 180° (南 S - SOUTH)
    "\n".join([
        "..#..",
        "..#..",
        "#.#.#",
        ".###.",
        "..#.."
    ]),
    # 225° (南西 SW - SOUTH_WEST)
    "\n".join([
        "....#",
        "...#.",
        "#.#..",
        "##...",
        "###.."
    ]),
    # 270° (西 W - WEST)
    "\n".join([
        "..#..",
        ".#...",
        "#####",
        ".#...",
        "..#.."
    ]),
    # 315° (北西 NW - NORTH_WEST)
    "\n".join([
        "###..",
        "##...",
        "#.#..",
        "...#.",
        "....#"
    ])
]

def get_led_pattern(frame):
    return frame.evaluate("""() => {
        const leds = document.querySelectorAll('rect.sim-led');
        let grid = [];
        for (let y = 0; y < 5; y++) {
            let row = '';
            for (let x = 0; x < 5; x++) {
                const led = Array.from(leds).find(l => {
                    const title = l.querySelector('title');
                    return title && title.textContent === `(${x},${y})`;
                });
                if (led) {
                    const style = led.getAttribute('style') || '';
                    const fill = led.getAttribute('fill') || '';
                    const isLit = style.includes('opacity: 1') || fill === '#ff0000' || fill === 'rgb(255, 0, 0)' || style.includes('opacity:1');
                    row += isLit ? '#' : '.';
                } else {
                    row += '.';
                }
            }
            grid.push(row);
        }
        return grid.join('\\n');
    }""")

def wait_for_log(page, logs, pattern, timeout_s=5.0):
    start_time = time.time()
    while time.time() - start_time < timeout_s:
        for log_msg in logs:
            if re.search(pattern, log_msg):
                return True
        page.wait_for_timeout(100)
    return False

def test_makecode_simulator_rotation():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    python_path = os.path.join(project_root, "sample-compass/src/compass_makecode.py")
    assert os.path.exists(python_path), f"compass_makecode.py exists at {python_path}"
    
    with open(python_path, "r", encoding="utf-8") as f:
        raw_python_code = f.read()
        
    # キャリブレーション状態チェックを強制バイパスし、すべての show_string を clear_screen に置き換える
    python_code = raw_python_code.replace("is_calibrated = False", "is_calibrated = True")
    python_code = re.sub(r"if not is_calibrated:", "if False:", python_code)
    python_code = re.sub(r"basic\.show_string\([^)]*\)", "basic.clear_screen()", python_code)
    
    print("Starting Playwright simulator rotation test for Python...")
    
    headless_mode = os.getenv("PLAYWRIGHT_HEADLESS", "1").lower() != "0"
    record_video = os.getenv("RECORD_VIDEO", "1").lower() == "1"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_mode)
        
        # ビデオ記録の設定
        context_opts = {
            "locale": "ja-JP",
            "accept_downloads": True,
        }
        
        if record_video:
            # ビデオ記録用ディレクトリ（sample-compass 配下）
            sample_compass_dir = os.path.join(project_root, "sample-compass")
            video_dir = os.path.join(sample_compass_dir, ".video-temp")
            os.makedirs(video_dir, exist_ok=True)
            context_opts["record_video_dir"] = video_dir
            print("🎬 Video recording enabled")
        else:
            print("⏭️  Video recording disabled")
        
        context = browser.new_context(**context_opts)
        page = context.new_page()
        
        # ブラウザ側のコンソールログを出力
        logs = []
        page.on("console", lambda msg: (print(f"[Browser Console] {msg.text}"), logs.append(msg.text)))
        
        try:
            # 1. MakeCode にアクセス
            page.goto("https://makecode.microbit.org/", wait_until="networkidle")
            time.sleep(2)
            
            # 2. 新しいプロジェクトを作成
            new_project_btn = page.locator('.ui.card:has-text("新しいプロジェクト"), .ui.card:has-text("New Project")').first
            new_project_btn.click(force=True)
            time.sleep(1)
            
            proj_name = f"compass-py-rot-test-{int(time.time() * 1000)}"
            page.locator("input#projectNameInput").fill(proj_name)
            
            create_btn = page.get_by_role("button", name="作成").or_(page.get_by_role("button", name="Create")).first
            create_btn.click(force=True)
            page.wait_for_load_state("networkidle")
            time.sleep(3)
            
            # チュートリアルポップアップなどのクリーンアップ
            page.evaluate("""() => {
                const selectors = [
                    '.teaching-bubble-container',
                    '.common-focus-trap',
                    '.ui.dimmer.active',
                    '.ui.modal.transition.visible'
                ];
                selectors.forEach(selector => {
                    const els = document.querySelectorAll(selector);
                    els.forEach(el => el.remove());
                });
            }""")
            time.sleep(0.5)
            
            # 3. Python エディタモードに切り替える
            try:
                page.locator(".python-menuitem").first.click(timeout=3000, force=True)
            except Exception:
                page.locator("#editordropdown").click(force=True)
                time.sleep(0.5)
                page.locator(".python-menuitem").first.click(force=True)
            time.sleep(2)
            
            # 4. Monaco エディタにソースコードを注入
            source_was_injected = page.evaluate("""(code) => {
                if (typeof window.monaco !== 'undefined') {
                    const models = window.monaco.editor.getModels();
                    const pyModel = models.find(m => m.uri.path.endsWith('.py') || m.uri.path.endsWith('main.py'));
                    if (pyModel) {
                        pyModel.setValue(code);
                        return true;
                    } else if (models && models.length > 0) {
                        models[0].setValue(code);
                        return true;
                    }
                }
                return false;
            }""", python_code)
            
            assert source_was_injected, "Source code was injected into monaco editor"
            time.sleep(3)
            
            # 5. ブロック表示に戻す
            try:
                page.locator(".blocks-menuitem").first.click(timeout=3000, force=True)
            except Exception:
                convert_btn = page.get_by_role("button", name="プログラムをブロックに変換する。").or_(page.get_by_role("button", name="Blocks")).first
                convert_btn.click(force=True)
            time.sleep(5)
            
            # 6. シミュレータのロード完了を待つ
            sim_iframe_locator = page.frame_locator('iframe[title*="Simulator"]')
            sim_svg = sim_iframe_locator.locator("svg").first
            sim_svg.wait_for(state="visible", timeout=15000)
            print("✓ Simulator loaded (Python)")
            
            # 7. 45度ずつ回転させて LED パターンをチェック
            headings = [0, 45, 90, 135, 180, 225, 270, 315]
            frame_element = page.locator('iframe[title*="Simulator"]').first.element_handle()
            frame = frame_element.content_frame()
            
            for i, heading in enumerate(headings):
                print(f"Setting heading to {heading}° (Python)...")
                frame.evaluate("""(h) => {
                    const board = window.pxsim.board();
                    board.compassState.heading = h;
                    board.updateView();
                }""", heading)
                
                time.sleep(1.2)  # 描画更新待ち
                
                led_pattern = get_led_pattern(frame)
                print(f"LED Pattern at {heading}° (Python):\n{led_pattern}")
                
                assert led_pattern == EXPECTED_PATTERNS[i], f"LED pattern mismatch at {heading}° (Python)"
                print(f"✓ Verified LED pattern for {heading}° (Python)")
                
                # Aボタンをクリックしてログをチェック
                logs.clear()
                btn_a = sim_iframe_locator.locator('.sim-button-group:has-text("A"), rect.sim-button-outer').first
                btn_a.click(force=True)
                
                direction = EXPECTED_DIRECTIONS[i]
                expected_log_pattern = rf"Time: \d+ms, Heading: {heading}, Dir: {direction}"
                
                # 最大5秒間ログ出力を待つ
                found = wait_for_log(page, logs, expected_log_pattern, timeout_s=5.0)
                assert found, f"Expected log '{expected_log_pattern}' not found in browser console logs. Current logs: {logs}"
                print(f"✓ Verified console log output for {heading}° (Python)")
                
            # 8. スクリーンショットを保存
            screenshot_dir = os.path.join(project_root, "dist")
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir, exist_ok=True)
            sim_iframe_locator.locator('.sim-embed, #board-container, svg.sim').first.screenshot(
                path=os.path.join(screenshot_dir, "rotation-test-py.png")
            )
            print(f"✓ Screenshot saved to {os.path.join(screenshot_dir, 'rotation-test-py.png')}")
            
        except Exception as e:
            error_screenshot_path = os.path.join(project_root, "error-rotation-py.png")
            page.screenshot(path=error_screenshot_path, full_page=True)
            print("Python Rotation Test failed. Saved screenshot to:", error_screenshot_path)
            raise e
        finally:
            # ビデオ確定のため context と browser を閉じる
            context.close()
            browser.close()
            
            # ビデオが確定されるまで少し待つ
            time.sleep(3)
            
            # デバッグ：ビデオディレクトリの確認
            sample_compass_dir = os.path.join(project_root, "sample-compass")
            video_temp = os.path.join(sample_compass_dir, ".video-temp")
            print(f"\n📁 Video temp dir: {video_temp}")
            print(f"📁 Video temp dir exists: {os.path.exists(video_temp)}")
            if os.path.exists(video_temp):
                files = os.listdir(video_temp)
                print(f"📁 Files in video temp: {files}")
            
            # ビデオを GIF に変換
            print("\n🎬 Converting video to GIF...")
            import subprocess
            import sys
            convert_script = os.path.join(project_root, "sample-compass/scripts/convert_video_to_gif.py")
            result = subprocess.run([sys.executable, convert_script], cwd=project_root, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
