# Firmwares ESP32: instalação pelo navegador

Site estático que usa o [ESP Web Tools](https://esphome.github.io/esp-web-tools/) para gravar firmwares no ESP32 direto pelo navegador.

## Publicar no GitHub Pages

1. Crie uma conta em https://github.com (se ainda não tiver).
2. Crie um repositório **público** (ex.: `canaldosnerds`).
3. Envie todos os arquivos desta pasta para o repositório
   (pelo site: "Add file" → "Upload files", arrastando as pastas).
4. No repositório, abra **Settings → Pages**.
   Em "Source" escolha **Deploy from a branch**, branch `main`, pasta `/ (root)`, e salve.
5. Em 1 ou 2 minutos o site fica no ar em `https://fabiopulzi.github.io/canaldosnerds/`.

## Adicionar um firmware

1. Crie uma pasta em `firmwares/` (ex.: `firmwares/meu-projeto/`).
2. Copie para ela os `.bin` gerados pelo build (veja abaixo onde ficam).
3. Copie o `manifest.json` do exemplo e ajuste o nome, a versão, o `chipFamily` e os arquivos.
4. No `index.html`, adicione um bloco na lista `firmwares`.

### Onde ficam os .bin

- **PlatformIO:** `.pio/build/<ambiente>/` contém `bootloader.bin`, `partitions.bin` e `firmware.bin`.
  O `boot_app0.bin` fica em `~/.platformio/packages/framework-arduinoespressif32/tools/partitions/`.
- **Arduino IDE:** Sketch → "Export Compiled Binary". Os arquivos aparecem na pasta `build/` do sketch.
  A IDE também gera um `*.merged.bin`, que já junta tudo.

### Alternativa mais simples: um único .bin

Se você tiver o arquivo "merged" (tudo junto), o manifest fica com uma parte só, no offset 0:

```json
"parts": [{ "path": "firmware.merged.bin", "offset": 0 }]
```

Para gerar com esptool:

```
esptool.py --chip esp32 merge_bin -o firmware.merged.bin \
  0x1000 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin 0x10000 firmware.bin
```

### Offsets por chip (bootloader)

| Chip | `chipFamily` | Offset do bootloader |
|---|---|---|
| ESP32 | `ESP32` | 0x1000 (4096) |
| ESP32-S2 | `ESP32-S2` | 0x1000 (4096) |
| ESP32-S3 | `ESP32-S3` | 0x0 (0) |
| ESP32-C3 | `ESP32-C3` | 0x0 (0) |

Os outros offsets (partições em 0x8000, boot_app0 em 0xe000, app em 0x10000) são os padrões do Arduino/PlatformIO.

Um mesmo manifest pode ter vários `builds`, um por chip. O site detecta o chip conectado e grava o build certo.
