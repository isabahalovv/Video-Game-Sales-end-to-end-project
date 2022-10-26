class Correlation_checker:
    def __init__(self, df, threshold):
        self.df = df
        self.threshold = threshold

    def check_by_threshold(self):

        df = self.df.copy()
        cols = df.columns
        extremes = []
        feats = []
        
        for x in cols:
            for y in cols:
                if x != y and abs(df.corr().loc[x, y]) > self.threshold:
                    extremes.append(df.corr().loc[x, y])
                    feats.append([x,y])
            
        print(extremes)
        return feats