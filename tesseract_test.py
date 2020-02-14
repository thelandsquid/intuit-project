import tesserocr
import excel_data_retrieval as excel
import time

def test_images(images, labels):
    correctForms, predictedForms = 0, 0
    times, accuracyPercentages = [], []
    with tesserocr.PyTessBaseAPI() as api:
        for i in range(len(images)):
            startTime = int(round(time.time() * 1000))
            api.SetImageFile(images[i])
            imageText = api.GetUTF8Text()
            predictionAmount, correctPredictions = 0, 0
            for j in range(1,len(labels[i])):
                labelStringArray = remove_label_and_marks(str(labels[i][j])).split()
                for labelStr in labelStringArray:
                    if labelStr in imageText:
                        correctPredictions+=1
                    # else:
                    #      print('Not recognized: ',labelStr)
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

def remove_label_and_marks(str):
    while str[0]!=':':
        str=str[1:]
    str=str[1:]
    if str[0]=='\'' and str[-1]=='\'':
        str = str[1:-1]
    if str[-2:]=='.0':
        str = str[:-2]
    return str

def main():
    #Clean Data
    print('CLEAN DATA')
    images = []
    for i in range(50):
        images.append('fifty-fifty-testing\\W2_XL_input_clean_'+str(1000+i)+'.jpg')
    labels = excel.get_labels_from_excel('fifty-fifty-testing\\labels.xlsx',0,1,50)
    test_images(images, labels)

    #Noisy Data
    print('NOISY DATA')
    images = []
    for i in range(50):
        images.append('fifty-fifty-testing\\W2_XL_input_noisy_' + str(1000 + i)+'.jpg')
    labels = excel.get_labels_from_excel('fifty-fifty-testing\\labels.xlsx',0,1,50)
    test_images(images, labels)

    # Single Test
    # images = ['fifty-fifty-testing\\W2_XL_input_clean_1000.jpg']
    # labels = excel.get_labels_from_excel('fifty-fifty-testing\\labels.xlsx', 0, 1, 1)
    # test_images(images, labels)

main()