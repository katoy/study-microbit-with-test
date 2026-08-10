# 動画チュートリアル台本: micro:bit方位磁石をテストする

想定尺は約18分です。画面には大きめのターミナル文字と字幕を表示し、テスト件数は台本へ固定せず、収録時の実行結果をそのまま見せます。

## 0:00〜1:00 オープニング

画面: micro:bit、MakeCodeブロック、Pythonテスト、TypeScriptテストを4分割表示。

ナレーション:

> この教材では、micro:bitの方位磁石をブロック、Python、TypeScriptの3つの視点から学びます。完成コードを見るだけでなく、22.5度の境界や未校正状態を自動テストで確かめます。

## 1:00〜3:00 全体構成

画面: ルートREADMEの「3つの実装」。

ナレーション:

> MakeCode版は実機とブロック、MakeCode Python版はPython構文とブラウザーシミュレーター、Node TypeScript版は型と純粋ロジックを担当します。Node版はそのままmicro:bitへ書き込むものではありません。

強調テロップ: 「シミュレーター ≠ 実機テスト」

## 3:00〜6:00 MakeCode

画面: `sample-compass-makecode/src/compass.ts`。

```typescript
_heading = input.compassHeading();
```

ナレーション:

> 磁北に対する方位角は `input.compassHeading()` で取得します。`input.acceleration` は傾きや加速度なので、方位磁石の代わりにはなりません。

画面: `main.ts` のボタンAと `basic.forever`。

> Aボタンで校正し、foreverループで方位を表示します。自動テストでは `setHeadingForTest` を使い、決まった値をシミュレーターへ与えます。

```bash
npm --prefix sample-compass-makecode test
```

末尾の成功結果を拡大します。

## 6:00〜10:00 MakeCode Pythonと境界値

画面: `sample-compass/src/compass_makecode.py` の方位判定。

```python
if heading < 22.5 or heading >= 337.5:
    return "N"
```

ナレーション:

> 北だけは0度を中心に360度をまたぎます。ここは典型的な境界バグの場所です。

画面: `sample-compass/test/test_simulator.py`。

```bash
npm run integration:python
```

> PCにはmicro:bitの磁気センサーがないため、このテストはMakeCode Webへソースを読み込み、シミュレーターの方位角を操作します。LED表示は確認できますが、実物のセンサー精度やUSB転送は保証しません。

## 10:00〜13:00 TypeScript

画面: `sample-compass-ts/src/compass.ts`。

```typescript
export type Direction = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW' | 'CAL' | 'ERR';
```

画面: `sample-compass-ts/test/compass.test.ts`。

```typescript
expect(Compass.headingToDirection(337.4)).toBe('NW');
expect(Compass.headingToDirection(337.5)).toBe('N');
```

ナレーション:

> TypeScriptでは戻り値の候補を型で限定できます。ただし `NaN` や `Infinity` もnumberなので、実行時検証は残ります。未校正状態は `CAL`、無効な値は `ERR` で知らせます。

```bash
npm --prefix sample-compass-ts run build
npm --prefix sample-compass-ts test
```

## 13:00〜16:00 品質ゲートとHEX

画面: ルートターミナル。

```bash
npm run test:all
npm run lint
npm run build:hex
```

ナレーション:

> `test:all` はルート設定、Python統合、TypeScript、MakeCodeシミュレーター、TypeScriptカバレッジの検査をまとめて実行します。実機用HEXのビルドはMakeCode版だけに対応しています。

画面: 生成先。

- `sample-compass-makecode/built/binary.hex`

## 16:00〜17:30 MakeCode Webで確認

ナレーション:

> ネットワーク接続がある環境では、生成したMakeCode HEXをMakeCode Webへ読み込み、TypeScriptとブロックの表示を確認します。MakeCode Pythonを試す場合は `sample-compass/src/compass_makecode.py` をPythonモードへ貼り付けます。

## 17:30〜18:00 まとめ

ナレーション:

> まず目で動きをつかみ、次に境界値をテストし、最後に実機で確認する。この順番なら、ハードウェアが手元にない時間も学習を進められます。続きは90分ワークショップと複数言語ガイドで試してください。

終了画面:

- `README.md`
- `WORKSHOP_TEMPLATE.md`
- `MULTILANGUAGE_GUIDE.md`
