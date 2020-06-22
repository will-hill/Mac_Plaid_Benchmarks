# Mac_Plaid_Benchmarks
Benchmarking PlaidML GPU accerlation of Keras on Macbook with Keras using MLFlow

> asciinema rec -i 2.0 mac_plaid.cast

python -m venv ~/py_envs/mac_plaid

source ~/py_envs/mac_plaid/bin/active

python -m pip install plaidml plaidml-keras plaidbench

plaidml-setup

cat simple.py

python -s simple.py



### Benchmarks

plaidbench
plaidbench --result ~/shuffle_results onnx --plaid shufflenet

plaidbench              \
--plaid | --caffe2 | --tf | --no-plaid \
--keras | --onnx        \
--fp16                  \
-v                      \
--results RESULTS       \
[--callgrind]           \
[--no-warmup]           \
[--no-kernel-timing]    \
-n EXAMPLES             \
--epochs EPOCHS         \
--batch-size BATCH_SIZE \
--train                 \
--blanket-run           \
--print-stacktraces     \
--onnx-cpu              \
--refresh-onnx-data     \
network