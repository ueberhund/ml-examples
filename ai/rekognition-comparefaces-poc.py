from os import system, name
import boto3
import time
from multiprocessing import Process


# POC code written to look through family photos and find who a specific person looks like
# The idea being that if you have 30 photos of relatives (both living and dead), you can run this
# code to see who the person in the image_to_compare looks the most like
# This code was split out into several threads to help with the speed

bucket_name = 'bucket_name'     #Replace with your bucket name
s3_prefix = 's3_prefix'         #Replace with your S3 prefix containing family images
image_to_compare = 'image.jpg'  #Replace with the person you want to do the comparisons for
max_threshold = 15              #Set a low max_threshold because we're comparing a person to other people--not
                                #other photos of themselves

def findMatch(fileName, key):
    try:
        rek_client = boto3.client('rekognition')
        match = rek_client.compare_faces(SourceImage={'S3Object':{'Bucket':bucket_name,'Name':fileName}},
                                TargetImage={'S3Object':{'Bucket':bucket_name,'Name':key}},
                                SimilarityThreshold=max_threshold)
        if len(match['FaceMatches']) > 0:
            print ('Face: %s (%4.2f%%)' % (key, match['FaceMatches'][0]['Similarity']))
        #else:
        #    print('Face: %s - NO MATCH' % (key))
    except:
        print('Invalid image %s' % (key))

#detect a face
def detectFace(prefix, fileName):
    #Check to see if the found face matches a face in our Rekognition database
    processes = []
    s3_client = boto3.client('s3')
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)

    #Loop over the photos in our bucket, but do this mutlithreaded to make it fast!
    for item in response['Contents']:
        p = Process(target=findMatch, args=(fileName, item['Key'],))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()


if __name__ == '__main__':
    start_time = time.time()

    detectFace(s3_prefix, image_to_compare)

    elapsed_time = time.time() - start_time
    print('Elapsed time: %d seconds' % (elapsed_time))
