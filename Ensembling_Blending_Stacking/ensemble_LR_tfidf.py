#########################################################################
# Ensemble model
#########################################################################

import pandas as pd 
from sklearn import linear_model
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer


def run_training(fold):
    df = pd.read_csv("/home/hasan/Desktop/ensembling_blending_stacking/train_folds.csv")
    #df.review = df.review.apply(str) 
    df_train = df[df.kfold != fold].reset_index(drop=True)
    df_valid = df[df.kfold == fold].reset_index(drop=True)


    tfv = TfidfVectorizer()
    tfv.fit(df_train.review.values)

    xtrain = tfv.transform(df_train.review.values)
    xvalid = tfv.transform(df_valid.review.values)

    ytrain = df_train.sentiment.values
    yvalid = df_valid.sentiment.values

    clf = linear_model.LogisticRegression()
    clf.fit(xtrain, ytrain)

    ypred = clf.predict_proba(xvalid)[:, 1]

    auc = metrics.roc_auc_score(yvalid, ypred)
    print(f"fold={fold}, auc={auc}")

    df_valid.loc[:, "lr_svd_pred"] = ypred

    return df_valid[["id", "sentiment", "kfold", "lr_svd_pred"]]


if __name__ == "__main__":
    dfs = []
    for j in range(5):
        temp_df = run_training(j)

        dfs.append(temp_df)
    fin_valid_df = pd.concat(dfs)
    print(fin_valid_df.shape)

    fin_valid_df.to_csv("/home/hasan/Desktop/ensembling_blending_stacking/svd_lr.csv", index=False)
