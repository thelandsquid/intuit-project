import tesserocr
import excel_data_retrieval as excel
import time
import argparse
import os, fnmatch

def image_accuracy_test(images, labels):
    correctForms, predictedForms = 0, 0
    times, accuracyPercentages = [], []
    with tesserocr.PyTessBaseAPI() as api:
        for i in range(len(images)):
            startTime = int(round(time.time() * 1000))
            api.SetImageFile(images[i])
            imageText = api.GetUTF8Text().lower()                   #converts the output of OCR to lowercase
            predictionAmount, correctPredictions = 0, 0
            for j in range(len(labels[i])):
                labelStringArray = (labels[i][j]).split('\\s')
                print(labelStringArray)
                for labelStr in labelStringArray:
                    if labelStr.lower() in imageText:                       #compare lowercase label with output of OCR
                        correctPredictions+=1
                    # else:
                    #      print('File: ', images[i],'|||Not recognized: ',labelStr)
                    predictionAmount+=1

            predictedForms+=1
            if correctPredictions/predictionAmount>.999999:
                correctForms+=1
            accuracyPercentages.append(correctPredictions/predictionAmount)
            times.append(int(round(time.time()*1000))-startTime)

    print('Forms Processed: ',predictedForms)
    print('Forms Properly Recognized: ',correctForms)
    print('Average Processing Time: ',sum(times)/len(times),' milliseconds')
    print('Average Cell Accuracy: ',100*sum(accuracyPercentages)/len(accuracyPercentages),'% of cells correctly recognized\n')

def test_fifty_fifty(clean_length, noisy_length):
    # Clean Data
    print('CLEAN DATA')
    images = []
    for i in range(clean_length):
        images.append('fifty-fifty-testing\\W2_XL_input_clean_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel('fifty-fifty-testing\\labels.xlsx', 0, 1, 50)
    image_accuracy_test(images, labels)

    # Noisy Data
    print('NOISY DATA')
    images = []
    for i in range(noisy_length):
        images.append('fifty-fifty-testing\\W2_XL_input_noisy_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel('fifty-fifty-testing\\labels.xlsx', 0, 1, 50)
    image_accuracy_test(images, labels)

def test_realistic_noise():
    # Realistic Noisy Data
    print('REALISTIC NOISY DATA')
    images = []
    for i in range(100):
        images.append('realistic-noise-testing\\W2_XL_input_noisy_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel('realistic-noise-testing\\labels.xlsx', 0, 1, 100)
    image_accuracy_test(images, labels)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images_path', type=str, required=False,
                        help='the path of the image set')
    parser.add_argument('-gt', '--ground_truth_path', type=str, required=False,
                        help='the path of the ground truth')
    args = parser.parse_args()
    if args.images_path is None:
        test_realistic_noise()
    elif args.ground_truth_path is None:
        print('Must provide both ground_truth_path (-gt) and images_path (-i)')
    else:
        images, labels = [], []
        onlyfiles = [f for f in os.listdir(args.images_path) if os.path.isfile(os.path.join(args.images_path, f))]
        for file_name in onlyfiles:
            if file_name.endswith(('.jpg','.jpeg','.gif','png')):
                file_name_template = file_name.split('.',1)[0]+'.gt'
                text_files = fnmatch.filter(os.listdir(args.ground_truth_path),file_name_template)
                if(len(text_files)!=1):
                    print('Improper amount of ground truth files for '+file_name)
                    exit(1)
                with open (os.path.join(args.ground_truth_path,text_files[0]),'r') as read_file:
                    data = read_file.readlines()
                    images.append(os.path.join(args.images_path,file_name))
                    labels.append(data)
        image_accuracy_test(images,labels)
main()