import tesserocr
import excel_data_retrieval as excel
import time

def image_accuracy_test(images, labels):
    correctForms, predictedForms = 0, 0
    times, accuracyPercentages = [], []
    with tesserocr.PyTessBaseAPI() as api:
        for i in range(len(images)):
            startTime = int(round(time.time() * 1000))
            api.SetImageFile(images[i])
            imageText = api.GetUTF8Text().lower()                   #converts the output of OCR to lowercase
            predictionAmount, correctPredictions = 0, 0
            for j in range(1,len(labels[i])):
                labelStringArray = remove_label_and_marks(str(labels[i][j])).split()
                for labelStr in labelStringArray:
                    if labelStr.lower() in imageText:                       #compare lowercase label with output of OCR
                        correctPredictions+=1
                    # else:
                    #      print('File: ', images[i],'|||Not recognized: ',labelStr)
                    predictionAmount+=1

            predictedForms+=1
            if correctPredictions/predictionAmount>.999999:
                correctForms+=1
            # print(correctPredictions/predictionAmount)
            accuracyPercentages.append(correctPredictions/predictionAmount)
            times.append(int(round(time.time()*1000))-startTime)

    print('Forms Processed: ',predictedForms)
    print('Forms Properly Recognized: ',correctForms)
    print('Average Processing Time: ',sum(times)/len(times),' milliseconds')
    print('Average Cell Accuracy: ',100*sum(accuracyPercentages)/len(accuracyPercentages),'% of cells correctly recognized\n')

# Removed labels added by excel document and removed decimals from integers (some numbers with .0 at end are integers in the W-2)
def remove_label_and_marks(str):
    while str[0]!=':':
        str=str[1:]
    str=str[1:]
    if str[0]=='\'' and str[-1]=='\'':
        str = str[1:-1]
    if str[-2:]=='.0':
        str = str[:-2]
    return str

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

# dataSet is clean=0, noisy=1
# imageNum corresponds to the code at the end of the image title
def test_fifty_fifty_single_image(dataSet, imageNum):
    switch = {
        0: 'clean',
        1: 'noisy',
        2: 'intermediate'
    }
    image = ['fifty-fifty-testing\\W2_XL_input_'+switch[dataSet]+'_'+str(1000+imageNum)+'.jpg']
    label = excel.get_labels_from_excel('fifty-fifty-testing\\labels.xlsx', dataSet, imageNum+1, 1)
    image_accuracy_test(image,label)

def main():
    CLEAN, NOISY, INTERMEDIATE = 0, 1, 2
    test_fifty_fifty_single_image(0, 0)
    test_fifty_fifty(50,50)
main()