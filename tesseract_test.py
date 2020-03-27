import tesserocr
import excel_data_retrieval as excel
import time
import argparse
import os, fnmatch

def image_accuracy_test(images, labels, results_path = None):
    perfect_forms = 0
    times, accuracyPercentages = [], []
    results_string = ''
    with tesserocr.PyTessBaseAPI() as api:
        for i in range(len(images)):
            startTime = int(round(time.time() * 1000))
            api.SetImageFile(images[i])
            results_string += images[i]+'\n'
            imageText = api.GetUTF8Text().lower()                   #converts the output of OCR to lowercase
            #print(imageText)
            correctPredictions = 0
            labelStringArray = (labels[i]).split()
            for labelStr in labelStringArray:
                if labelStr.lower() in imageText:                       #compare lowercase label with output of OCR
                    correctPredictions+=1
                else:
                    results_string += '\tNot recognized: '+labelStr+'\n'

            local_accuracy = correctPredictions/len(labelStringArray)
            if local_accuracy>.999999:
                perfect_forms+=1
            accuracyPercentages.append(local_accuracy)
            results_string += '\tWord Accuracy: '+str(local_accuracy)+'\n'
            times.append(int(round(time.time()*1000))-startTime)

    print('Forms Processed: ',len(images))
    print('Forms Perfectly Recognized: ',perfect_forms)
    print('Average Processing Time: ',sum(times)/len(times),' milliseconds')
    print('Average Cell Accuracy: ',100*sum(accuracyPercentages)/len(accuracyPercentages),'% of cells correctly recognized\n')
    if results_path!=None:
        output_results(results_path,results_string)

def output_results(results_path,results_string):
    print()
    try:
        with open(results_path, "w") as text_file:
            text_file.write(results_string)
        print("Output results to: ",results_path)
    except FileNotFoundError:
        print('\nError writing results to text file')
        print('Results dumped to results_ocr.txt in working directory')
        with open('results_ocr.txt', "w") as text_file:
            text_file.write(results_string)

def test_fifty_fifty(clean_length, noisy_length):
    project_root = os.path.dirname(__file__)
    if(project_root!=''):
        project_root+='/'

    # Clean Data
    print('CLEAN DATA')
    images = []
    for i in range(clean_length):
        images.append(str(project_root)+'fifty-fifty-testing/W2_XL_input_clean_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel(str(project_root)+'fifty-fifty-testing/labels.xlsx', 0, 1, 50)
    image_accuracy_test(images, labels)

    # Noisy Data
    print('NOISY DATA')
    images = []
    for i in range(noisy_length):
        images.append(str(project_root)+'fifty-fifty-testing/W2_XL_input_noisy_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel(str(project_root)+'fifty-fifty-testing/labels.xlsx', 0, 1, 50)
    image_accuracy_test(images, labels)

def test_realistic_noise(output_file=None):
    project_root = os.path.dirname(__file__)
    if (project_root != ''):
        project_root += '/'

    # Realistic Noisy Data
    print('REALISTIC NOISY DATA')
    images = []
    for i in range(100):
        images.append(str(project_root)+'realistic-noise-testing/W2_XL_input_noisy_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel(str(project_root)+'realistic-noise-testing/labels.xlsx', 0, 1, 100)
    image_accuracy_test(images, labels,output_file)

def test_realistic_noise_distinct_path(distinct_path,output_file=None):
    project_root = os.path.dirname(__file__)
    if (project_root != ''):
        project_root += '/'

    # Realistic Noisy Data
    print('REALISTIC NOISY DATA')
    images = []
    for i in range(100):
        images.append(str(project_root)+'realistic-noise-testing/W2_XL_input_noisy_' + str(1000 + i) + '.jpg')
    labels = excel.get_labels_from_excel(str(project_root)+'realistic-noise-testing/labels.xlsx', 0, 1, 100)
    image_accuracy_test(images, labels,output_file)

def main():
    print(os.path.dirname(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--images_path', type=str, required=False,
                        help='the path of the image set')
    parser.add_argument('-gt', '--ground_truth_path', type=str, required=False,
                        help='the path of the ground truth')
    parser.add_argument('-o', '--output', type=str, required=False,
                        help='the path of the results output file')
    parser.add_argument('-r', '--realistic', action='store_true',required=False,
                        help='the option to have realistic data set testing with an image path')
    args = parser.parse_args()
    if args.images_path is None and args.realistic is None:
        test_realistic_noise(args.output)
    elif args.realistic is not None:
        if args.images_path is None:
            print('Must provide image path for testing against realistic ground truth')
        else:
            test_realistic_noise_distinct_path(args.images_path,args.output)
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
                    data = read_file.read()
                    images.append(os.path.join(args.images_path,file_name))
                    labels.append(data)
        image_accuracy_test(images,labels,args.output)
main()