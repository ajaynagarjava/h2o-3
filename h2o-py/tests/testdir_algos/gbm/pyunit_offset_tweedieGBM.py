import sys
sys.path.insert(1, "../../../")
import h2o

def offset_tweedie(ip,port):
    # Connect to a pre-existing cluster
    h2o.init(ip,port)

    insurance = h2o.import_frame(h2o.locate("smalldata/glm_test/insurance.csv"))

    insurance["offset"] = insurance["Holders"].log()

    gbm = h2o.gbm(x=insurance[0:3], y=insurance["Claims"], distribution="tweedie", ntrees=600, max_depth=1, min_rows=1,
                  learn_rate=.1, offset_column=insurance["offset"], training_frame=insurance)

    predictions = gbm.predict(insurance)

    # Comparison result generated from harrysouthworth's gbm:
    #	fit2 = gbm(Claims ~ District + Group + Age+ offset(log(Holders)) , interaction.depth = 1,n.minobsinnode = 1,shrinkage = .1,bag.fraction = 1,train.fraction = 1,
    #           data = Insurance, distribution ="tweedie", n.trees = 600)
    #	pr = predict(fit2, Insurance)
    #	pr = exp(pr+log(Insurance$Holders))


    print " abs(-1.869702 - gbm._model_json['output']['init_f']) "
    print abs(-1.869702 - gbm._model_json['output']['init_f'])

    print " abs(49.21591 - predictions.mean()) "
    print abs(49.21591 - predictions.mean())

    print " abs(1.0258 - predictions.min()) "
    print abs(1.0258 - predictions.min())

    print " abs(392.4651 - predictions.max()) "
    print abs(392.4651 - predictions.max())


if __name__ == "__main__":
    h2o.run_test(sys.argv, offset_tweedie)
