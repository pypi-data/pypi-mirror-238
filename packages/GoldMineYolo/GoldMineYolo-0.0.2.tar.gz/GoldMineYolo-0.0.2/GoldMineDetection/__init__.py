def one_image(imagePath):
    print(imagePath)
    return model.predict(source=imagePath, save=True, conf=.45)