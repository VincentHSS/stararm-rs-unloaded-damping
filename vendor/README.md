# Private Smart Servo SDK

This project uses its own `motorbridge-smart-servo` overlay. It does not install
or replace a package in the shared `lerobot` environment.

`motorbridge-smart-servo/` is based on the locally patched upstream 0.0.4 SDK
(`0.0.4+rsfix1`, upstream commit `319649f0b89d0aa247d8862ca4c4c72c198e6d90`,
author tianrking, MIT). The existing rsfix1 serial and zero-sample behavior is
preserved. This copy adds `FashionStarServo.set_damping(servo_id, power)` and is
versioned `0.0.4+rsfix1.damping1`.

Upstream's source release declares MIT but does not include a standalone license
file or copyright notice. The supplied declarations and checked source are
recorded in [LICENSE-NOTICE.md](motorbridge-smart-servo/LICENSE-NOTICE.md).

The added method sends the supplied `fs102hd_damping.py` opcode **0x09**, with
parameters `[id, power_low, power_high]`, through the existing native controller
and its mutex. It shares the Leader plugin's one serial connection with monitor,
HOLD and unlock commands. It is distinct from opcode 0x18 `set_stop_mode`.
Successful writing is not an acknowledgement from servo firmware.

The built wheel is in `wheels/`; its package is extracted into `runtime/`. Prepend
the absolute `vendor/runtime` path to the **new project's subprocess** `PYTHONPATH`
before importing the Leader plugin. The shared installation remains untouched.

To rebuild with Rust, Maturin and the target Python available:

```bash
cd vendor/motorbridge-smart-servo
cargo test --locked -p smart_servo_core -p smart_servo_vendor_fashionstar
maturin build --locked --release --interpreter /path/to/lerobot/bin/python --out ../wheels
```

Extract the resulting wheel's `motorbridge_smart_servo/` and `.dist-info/`
directories into `vendor/runtime` with Python's `zipfile`, without `pip install`.
Run the PTY tests with the overlay on `PYTHONPATH`:

```bash
PYTHONPATH="$PWD/vendor/runtime" /path/to/lerobot/bin/python -m unittest discover \
  -s vendor/motorbridge-smart-servo/tests -v
```

All transport tests use OS pseudo-terminals. They do not open physical hardware.
