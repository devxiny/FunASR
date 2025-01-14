from funasr import AutoModel

model = AutoModel(model="outputs")

res = model.export(quantize=False)
# import onnx

# print("ONNX version:", onnx.__version__)