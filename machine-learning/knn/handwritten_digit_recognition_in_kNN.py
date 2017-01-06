import numpy as np
from os import listdir
import operator
import time

# img2vector ����
# �������ļ���
# ���أ�numpy ����
# ���ܣ��� 32x32 �Ķ�����ͼ�����ת��Ϊ 1x1024 ������


def img2vector(file):
    returnVec = np.zeros((1, 1024))
    with open(file) as fr:
        for i in range(32):
            lineStr = fr.readline()
            for j in range(32):
                returnVec[0, 32*i+j] = int(lineStr[j])
    return  returnVec
	
# classify ���෽��
# ���ܣ��Դ������ݽ��з���
# ������
#    inX������������
#    dataSet��ѵ�����ݼ�
#    labels����ǩ����
#    k����������
# ���أ����ǩ

def classify(inX, dataSet, labels, k=3):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize,1)) - dataSet   # tile(A,n) -- �������� A �ظ�n�� 
    sqDiffMat = np.power(diffMat, 2)
    sqDistance = sqDiffMat.sum(axis=1)
    distance = np.sqrt(sqDistance)
    sortedDistIndicies = distance.argsort()
    classCount = {}
    for i in range(k):
        voteLabel = labels[sortedDistIndicies[i]]
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
	

# ��ȡͼ�������ļ���ת���ɾ���
def read_and_convert(filePath):
    dataLabel = []
    fileList = listdir(filePath)
    fileAmount = len(fileList)
    dataMat = np.zeros((fileAmount, 1024))
    for i in range(fileAmount):
        fileNameStr = fileList[i]
        classTag = int(fileNameStr.split(".")[0].split("_")[0])
        dataLabel.append(classTag)
        dataMat[i,:] = img2vector(filePath+"/{}".format(fileNameStr))
    return dataMat, dataLabel

	
# ��д����ʶ��
def handwrittingClassify():
    hwlabels = []
    trainFilePath = "trainingDigits"
    trainFileList = listdir(trainFilePath)
    m = len(trainFileList)
    trainMat = np.zeros((m, 1024))
    st = time.clock()
    for i in range(m):
        fileNameStr = trainFileList[i]
        fileStr = fileNameStr.split(".")[0]
        classNum = int(fileStr.split("_")[0])
        hwlabels.append(classNum)
        #fpath = trainFilePath + "/" + fileNameStr
        trainMat[i,:] = img2vector(trainFilePath+"/{}".format(fileNameStr))
    #return trainMat, hwlabels
    testFilePath = "testDigits"
    testFileList = listdir(testFilePath)
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split(".")[0]
        classNum = int(fileStr.split("_")[0])
        vectorTest = img2vector(testFilePath+"/{}".format(fileNameStr))
        classifyResult = classify(vectorTest, trainMat, hwlabels, 3)
        #print("the classifier came back with: {0}, the real answer is: {1}".format(classifyResult, classNum))
        if (classifyResult != classNum):
            errorCount += 1.0
    et = time.clock()
    print("cost {:.4f} s".format(et-st))
    print("the total numbers of error is: {}".format(errorCount))
    print("the total error rate is: {:.6f}".format(errorCount/float(mTest)))


	
	
