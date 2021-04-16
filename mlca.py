def generate(center_cell, max_state, survive_arr, born_arr):
    live_cells_count = np.sum((neighborhood == max_state).astype(int))
        if center_cell == max_state: 
            for num_neighbors in survive_arr:
                if live_cells_count - 1 == num_neighbors: 
                    return center_cell 
            return center_cell – 1
        else if center_cell != 0 and center_cell != max_state:
            return center_cell – 1
        else:
            for num_neighbors in born_arr: 
                if total == num_neighbors:
                    return max_state 
            return 0


def frame_extraction(file_path):
    frames_list = []
    for x in range(80, 120):
        image = cv2.imread(file_path + str(x) + ".png", cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        frames_list.append(image)




model_name="nasnetalarge"
model=pretrainedmodels.__dict__[model_name](num_classes=1000, pretrained='imagenet')
model.eval()
load_img = utils.LoadImage()
tf_img = utils.TransformImage(model)
features_file = open("file.csv", "ab")
feature_data = []
for i in range(len(image_paths)):
    input_img = load_img(image_paths[i])
    input_tensor = tf_img(input_img)
    input_tensor = input_tensor.unsqueeze(0)
    input = torch.autograd.Variable(input_tensor, requires_grad=False)
    output_logits = model(input)
    output_features = model.features(input)
    output_logits = model.logits(output_features)
    output_logits = output_logits[0].detach().numpy()
    row_data = np.append(output_logits, labels[i])
    feature_data = np.append(feature_data, row_data)

def extract_features(IMAGE_DIR): 
    img_array = cv2.imread(IMAGE_DIR, cv2.IMREAD_GRAYSCALE)
    feature = np.reshape(new_array, (new_array.shape[0]*new_array.shape[1]))
    feature_extraction_data.append([feature, class_num])    


def COMPUTE_ENTROPY(signal)
    lensig = signal.size
    symset = list(set(signal))
    probpab = [np.size(signal[signal == i]) / (1.0 * lensig) for i in symset]
    entropy = np.sum([p * np.log2(1.0 / p) for p in  propab])
    return entropy






requests.post("https://api.mailgun.net/v3/sandbox7c2762c961a542a7a94ee770e53f6dfe.mailgun.org/messages", 
                                                        auth=("api", "key-8df5573973017338e393a6dae8f3b814"),
                                                        data={"from": "Excited User <mailgun@sandbox7c2762c961a542a7a94ee770e53f6dfe.mailgun.org>",
                                                        "to": [email_address],
                                                        "subject": "Your task has been completed",
                                                        "text": "Task has been completed!"})    


requests.post(
        "https://api.mailgun.net/v3/sandbox7c2762c961a542a7a94ee770e53f6dfe.mailgun.org/messages",
        auth=("api", "key-8df5573973017338e393a6dae8f3b814"),
        data={"from": "Excited User <mailgun@sandbox7c2762c961a542a7a94ee770e53f6dfe.mailgun.org>",
            "to": ["liaoqitian1024@gmail.com"],
            "subject": "Hello",
            "text": "Testing some Mailgun awesomness!"})


