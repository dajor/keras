from keras import applications
vgg = applications.VGG16(include_top=True, weights='models/images_model', classes=16)
#vgg1 = applications.VGG16(include_top=True, weights='./vgg16_weights_th_dim_ordering_th_kernels_Holistic_91.11.h5', classes=16)
import numpy as np
import numpy as np
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input

 

class_map = ['letter', 'form', 'email', 'handwritten', 'advertisement',
    'scientific report', 'scientific publication', 'specification', 'file folder',
    'news article', 'budget', 'invoice', 'presentation', 'questionnaire',
    'resume', 'memo']

 

def test(path):
    img = image.load_img(path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
    x = np.expand_dims(img, 0)
    y = vgg.predict(x)
    print(y)

 

    idx = np.argmax(y)
    print('predicted class: {}', class_map[idx])
    
    y = vgg1.predict(x)
    print(y)

 

    idx = np.argmax(y)
    print('predicted class: {}', class_map[idx])

 

test('./1.jpg')
 
