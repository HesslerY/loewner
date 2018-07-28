import matlab.engine
eng = matlab.engine.start_matlab()

t = eng.test(lambda x: x * 2,2)
print(t)
