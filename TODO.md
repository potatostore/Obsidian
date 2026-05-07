typedef struct Score {  
    int MathScore;  
    int EngScore;  
    int PhyScore;  
    int ArtScore;  
    int MusicScore;  
} Score;  
  
void processScore(){  
    Score score;  
    getScore(score);  
    int total = calculateSum(score);  
    double average = ccalculateSumAverage(Score);  
    print(S_ID, total, average);  
}  
  
double calculateSumAverage(Score score){  
    int total = calculateSum(score);  
    double average = total / count(score);  
	return average;  
}