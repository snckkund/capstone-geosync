import geemap
import ee

def classify_image():
    # Initialize GEE
    ee.Authenticate()
    ee.Initialize(project='ee-geosynta')

    # Define the region of interest (ROI)
    ddn = ee.Geometry.Polygon(
        [[77.70336408729965, 30.55530016444844],
         [77.70336408729965, 30.059720911875814],
         [78.39000959511215, 30.059720911875814],
         [78.39000959511215, 30.55530016444844],
         [77.70336408729965, 30.55530016444844]]  # Closing the polygon by repeating the first point
    )

    # Load Sentinel-2 image collection
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    s2_ddn_2023 = s2.filterDate('2023-01-01', '2023-12-31') \
                    .filterBounds(ddn) \
                    .median()
    bands = ['B2', 'B3', 'B4', 'B8']
    s2_ddn_2023 = s2_ddn_2023.select(bands).addBands(s2_ddn_2023.normalizedDifference(['B8', 'B4']).rename('NDVI'))

    # Define training data
    Forest = ee.FeatureCollection(
        [ee.Feature(ee.Geometry.Point([77.82375031706329, 30.41057315086976]), {"Class": 1}),
         ee.Feature(ee.Geometry.Point([77.85670930143829, 30.4209356983649]), {"Class": 1}),
         ee.Feature(ee.Geometry.Point([77.90690107605175, 30.37666338341595]), {"Class": 1}),
         ee.Feature(ee.Geometry.Point([77.92338056823925, 30.358890289808382]), {"Class": 1}),
         ee.Feature(ee.Geometry.Point([77.71007473341443, 30.39166406628676]), {"Class": 1}),
         ee.Feature(ee.Geometry.Point([77.74784023634412, 30.377151842407613]), {"Class": 1}),
         ee.Feature(ee.Geometry.Point([77.91354225400153, 30.271058411265834]), {"Class": 1})
        ]
    )
    Water = ee.FeatureCollection(
        [ee.Feature(ee.Geometry.Point([78.2798434702323, 30.061130035170603]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.30302467855122, 30.102029593376386]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.31244603810026, 30.12212076669471]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.25071645278393, 30.14807448469483]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.21213679672582, 30.19797006697161]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.18002502114881, 29.959676905547642]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.4358501452102, 30.436724213601458]), {"Class": 2}),
         ee.Feature(ee.Geometry.Point([78.57105962376131, 30.37480549185768]), {"Class": 2})
        ]
    )
    Urban = ee.FeatureCollection(
        [ee.Feature(ee.Geometry.Point([77.88316335793434, 29.877719647778548]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([77.89998617287574, 29.86283394173815]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([77.8405932425956, 29.907000582231795]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([77.81673231119912, 29.882742865797542]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([78.0588360841092, 29.96415962545435]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([78.07153902600373, 29.949286835454412]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([77.54934511731233, 29.977245839821535]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([77.53732882092561, 29.946014523071565]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([78.07560275632922, 30.45737311413907]), {"Class": 3}),
         ee.Feature(ee.Geometry.Point([78.08307002622668, 30.453599723809234]), {"Class": 3})
        ]
    )

    training = Water.merge(Forest).merge(Urban)
    trainingImage = s2_ddn_2023.sampleRegions(collection=training, properties=['Class'], scale=10)
    trainingData = trainingImage.randomColumn()
    trainSet = trainingData.filter(ee.Filter.lessThan('random', 0.8))
    testSet = trainingData.filter(ee.Filter.greaterThanOrEquals('random', 0.8))

    # Train a random forest classifier with specified parameters
    classifier = ee.Classifier.smileRandomForest(numberOfTrees=100).train(trainSet, 'Class', bands)
    classified = s2_ddn_2023.classify(classifier)

    # Sample prediction for demo purposes
    result = {
        'classification': 'Demo Result',
        'accuracy': 'Accuracy details here'
    }

    # Extracting accuracy metrics
    trainAccuracy = classifier.confusionMatrix()
    result['training_error_matrix'] = trainAccuracy.getInfo()
    result['training_accuracy'] = trainAccuracy.accuracy().getInfo()

    testSet = testSet.classify(classifier)
    validationAccuracy = testSet.errorMatrix('Class', 'classification')
    result['validation_error_matrix'] = validationAccuracy.getInfo()
    result['validation_accuracy'] = validationAccuracy.accuracy().getInfo()

    return result