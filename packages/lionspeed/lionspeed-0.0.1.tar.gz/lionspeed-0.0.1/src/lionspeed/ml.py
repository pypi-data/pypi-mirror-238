ass1 = """#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline 


df=pd.read_csv("heart.csv")

df.head()

print(df.shape)

df.isnull().sum()

df.tail()

df.info()

df.describe()

df.fillna(246.002933)

df.dtypes['age']

df.isnull()

df.drop('target',axis='columns')

df.drop(4)

df.iloc[1:6,2:4]

df.loc[1:6]

df.drop_duplicates()

df.fillna(df.mean())

df['age'].mean()

df.drop_duplicates().sum()

df.drop_duplicates(subset=['ca'])``

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns

sns.distplot(df['chol'],kde=False,bins=10,color='violet')

plt.figure(figsize=(8,6))
sns.countplot(x='age',hue='target',data=df,color='pink')
plt.show()

print(df.to_string())

df1 = df.fillna(df.median())
print(df1.to_string())

df1.drop_duplicates()

df = df1.astype({'trestbps':'int','chol':'int','oldpeak':'int','slope':'int'})
df

X = df.drop('target',axis = 'columns')
y = df["target"]

X

y

x_train,x_test, y_train, y_test = train_test_split(X,y,test_size = 0.25)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

Reg = LogisticRegression()

Reg.fit(x_train, y_train)

y_predict = Reg.predict(x_test)

y_predict.shape

print(accuracy_score(y_test, y_predict))

print(classification_report(y_test, y_predict))

print(classification_report(y_test, y_predict))

print(confusion_matrix(y_test, y_predict))

sns.heatmap(confusion_matrix(y_test, y_predict),annot = True)


"""
ass2 = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn import metrics

df=pd.read_csv("weight-height.csv")
df

x=df.iloc[:,1:2]
y=df.iloc[:,2]
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25)
Reg = LinearRegression()
Reg.fit(x_train,y_train)

Y_predict = Reg.predict(x_test)

Y_predict.shape

print(Reg.coef_)

print(Reg.intercept_)

plt.scatter(x_test,y_test,color='green')

print('Mean Square Error',metrics.mean_squared_error(y_test, Y_predict))

print('Mean Absolute Error',metrics.mean_absolute_error(y_test, Y_predict))

rsquare = Reg.score(x_train, y_train)
rsquare

"""

ass3 =""" import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

df=pd.read_csv("Admission_Predict.csv")
df

df.to_string()

df.isna().sum()

df.columns=df.columns.str.rstrip()
df.loc[df['Chance of Admit']>=0.8,'Chance of Admit']=1
df.loc[df['Chance of Admit']<=0.8,'Chance of Admit']=0

x=df.iloc[:,1:7]
y=df.iloc[:,8]
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25)
model=DecisionTreeClassifier(criterion='entropy')
model.fit(x_train,y_train)

Y_predict = model.predict(x_test)

print(accuracy_score(y_test, Y_predict)) 

print(classification_report(y_test,Y_predict))

print(confusion_matrix(y_test, Y_predict))

sns.heatmap(confusion_matrix(y_test, Y_predict),annot = True)

feature_names=df.iloc[0:8]
print(feature_names,end='')

target_name=[str(x) for x in model.classes_]
target_name

from sklearn.tree import plot_tree
fig=plt.figure(figsize=(50,30))

plot_tree(model)

plt.savefig("Decision_tree_visualization.png")

x=df.iloc[:,1:7]
x

from sklearn import tree

sf= StratifiedKFold(n_splits=5,shuffle=True,random_state=0)

depth=[1,2,3,4,5,6,7,8,9,10]

for d in depth:
    score=cross_val_score(tree.DecisionTreeClassifier(criterion='entropy',max_depth=d,random_state=0),x_train,y_train,cv=sf,scoring='accuracy')
    print('Average score for depth  is : '.format(d,score.mean()))

"""


ass4 =""" import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("mall.csv")

df

df.shape

df.info()

X=df.iloc[:,[3,4]].values

X

from sklearn.cluster import KMeans

wcss=[]

for i in range(1,11):
    kmeans=KMeans(n_clusters=i,init='k-means++',max_iter=300,random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
    
plt.plot(range(1,11),wcss)
plt.title('elbow method')
plt.xlabel('number of clusters')
plt.ylabel('wcss')

kmeans=KMeans(n_clusters=5,init='k-means++',max_iter=300,random_state=42)
y_kmeans=kmeans.fit_predict(X)

y_kmeans

y_kmeans.shape

plt.scatter(X[y_kmeans==0,0],X[y_kmeans==0,1],s=200,c='red',label='cluster1')
plt.scatter(X[y_kmeans==1,0],X[y_kmeans==1,1],s=200,c='blue',label='cluster2')
plt.scatter(X[y_kmeans==2,0],X[y_kmeans==2,1],s=200,c='green',label='cluster3')
plt.scatter(X[y_kmeans==3,0],X[y_kmeans==3,1],s=200,c='magenta',label='cluster4')
plt.scatter(X[y_kmeans==4,0],X[y_kmeans==4,1],s=200,c='pink',label='cluster5')
plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:,1],s=300,c='yellow',label='centroid')
plt.title("kmeans clustering")
plt.xlabel("annual income")
plt.ylabel("spending score")
plt.legend()
plt.show()

import matplotlib.cm as cm
from sklearn.metrics import silhouette_samples,silhouette_score

range_n_clusters=[2,3,4,5,6]
for n_clusters in range_n_clusters:
    clusterer=KMeans(n_clusters=n_clusters,random_state=10)
    cluster_labels=clusterer.fit_predict(X)
    
    silhouette_avg=silhouette_score(X,cluster_labels)
    print("for n_clusters=",n_clusters,"the average silhouette_score is ",silhouette_avg)

    

import scipy.cluster.hierarchy as sch
plt.figure(figsize=(10,10))
dendrogram=sch.dendrogram(sch.linkage(X,method='single'))
plt.title('dendrogram')
plt.xlabel('customers')
plt.ylabel('euclidean distances')
plt.show()

from sklearn.cluster import AgglomerativeClustering
hc=AgglomerativeClustering(n_clusters=5,affinity='euclidean',linkage='complete')
y_hc=hc.fit_predict(X)

plt.figure(figsize=(8,8))
plt.scatter(X[y_hc==0,0],X[y_hc==0,1],s=100,c='red',label='careful customers')
plt.scatter(X[y_hc==1,0],X[y_hc==1,1],s=100,c='blue',label='standard customers')
plt.scatter(X[y_hc==2,0],X[y_hc==2,1],s=100,c='green',label='target customers')
plt.scatter(X[y_hc==3,0],X[y_hc==3,1],s=100,c='cyan',label='careless customers')
plt.scatter(X[y_hc==4,0],X[y_hc==4,1],s=100,c='magenta',label='sensible customers')
plt.title("clusters of customer using hierarchical clustering")
plt.xlabel("annual income")
plt.ylabel("spending score")
plt.legend()
plt.show()


"""

ass5 =""" import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

df = pd.read_csv('pima-indians-diabetes.csv')

df

df.info()

X=df.iloc[:0:-1].values
X

y=df.iloc[:,8].values
y


model=Sequential()
model.add(Dense(12,input_dim=8,activation='relu'))
model.add(Dense(8,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.fit(X,y,epochs=150,batch_size=10)
accuracy=model.evaluate(X,y)
print("accuracy: .2f" % (accuracy*100))
from ann_visualizer.visualize import ann_viz;
ann_viz(model,title='my first neural network')

"""

daaks =""" #include<bits/stdc++.h>
using namespace std;

double fractionalKnapsack(int W, int n, vector<int>&  weights, vector<int>& values);
int boundedKnapsack(int W, int n, vector<int>&  weights, vector<int>& values);
void whichIsBetter(int W, int n, vector<int>&  weights, vector<int>& values);

int main() {

    int option = 1;
    while(option) {
        
        int W;
        cout << "Enter capacity of the Knapsack: ";
        cin >> W;

        int n;
        cout << "Enter number of items: ";
        cin >> n;
        
        vector<int> weights;
        cout << "Enter weights of n items: ";
        for(int i=0; i<n; i++) {
            int wt;
            cin >> wt;
            weights.push_back(wt);
        }

        vector<int> values;
        cout << "Enter price of n items: ";
        for(int i=0; i<n; i++) {
            int price;
            cin >> price;
            values.push_back(price);
        }    

        cout << "1. Fractional Knapsack   2. 0/1 Knapsack   3. Both (comparison)   0. Exit ";
        cout << "Enter your choice: ";
        cin >> option;

        switch (option) {
            case 1: fractionalKnapsack(W, n, weights, values);
                    break;
            case 2: boundedKnapsack(W, n, weights, values);
                    break;
            case 3: whichIsBetter(W, n, weights, values);
                    break;
            case 0: cout << "----- Thank you! ----";
                    break;
            default: cout << "Invalid choice!";
                    break;
        }
    }
    return 0;
}

double fractionalKnapsack(int W, int n, vector<int>&  weights, vector<int>& values) {
    vector< pair <double, int> > pricePerKg;  // pair: weight_per_kg & respective_index
    for(int i=0; i<n; i++) {
        double average = values[i]/(double)weights[i];
        pricePerKg.push_back(make_pair(average, i));
    }
    sort(pricePerKg.begin(), pricePerKg.end());
    double profit = 0;
    double capacity = 0;
    for(int i=n-1; i>=0; i--) {
        int index = pricePerKg[i].second;
        double p = pricePerKg[i].first;
        if(capacity == W) {
            break;
        }
        if(W >= capacity+weights[index]) {
            profit += values[index];
            capacity += weights[index];
        }
        else {
            double total_wt = 0;
            while(capacity+1 <= W) {
                capacity += 1;
                total_wt += 1;
                profit += p;
                if(total_wt == weights[index]) {
                    break;
                }
            }
            break;
        }
    }
    cout << profit << endl;
    return profit;
}
int boundedKnapsack(int W, int n, vector<int>&  weights, vector<int>& values) {
    int dp[n+1][W+1];
	memset(dp, -1, sizeof(dp));
	for(int i=0; i<=n; i++) {
		for(int j=0; j<=W; j++) {
			if(i*j == 0) {
				dp[i][j] = 0;
			} 
		}
	}
	for(int i=1; i<=n; i++) {
		for(int j=1; j<=W; j++) {
			if(weights[i-1] <= j) {
				dp[i][j] = max(values[i-1]+dp[i-1][j-weights[i-1]], dp[i-1][j]);
			} 
			else {
				dp[i][j] = dp[i-1][j];
			}
		}
	}
    cout << dp[n][W] << endl;
	return dp[n][W];
}
void whichIsBetter(int W, int n, vector<int>&  weights, vector<int>& values) {
    int a = boundedKnapsack(W, n, weights, values);
    double b = fractionalKnapsack(W, n, weights, values);
    if(a == b) {
        cout << "SAME RESULTS";
    }
    else if(a> b) {
        cout << "0/1knapsack is better";
    }
    else {
        cout << "fractional knapsack is better";
    }
}
// output:
/*
Enter capacity of the Knapsack: 12
Enter number of items: 5
Enter weights of n items: 1 2 3 4 5
Enter price of n items: 4 2 6 1 2
1. Fractional Knapsack   2. 0/1 Knapsack   3. Both (comparison)   0. Exit
Enter your choice: 3
14
14.25
fractional knapsack is better
*/

/*
Enter capacity of the Knapsack: 20
Enter number of items: 6
Enter weights of n items: 4 4 2 1 6 3
Enter price of n items: 6 7 4 3 9 5
1. Fractional Knapsack   2. 0/1 Knapsack   3. Both (comparison)   0. Exit
Enter your choice: 3
34
34
SAME RESULTS
*/

/*
Enter capacity of the Knapsack: 10
Enter number of items: 4
Enter weights of n items: 1 2 3 4
Enter price of n items: 4 2 6 1
1. Fractional Knapsack   2. 0/1 Knapsack   3. Both (comparison)   0. Exit
Enter your choice: 3
13
13
SAME RESULTS
*/"""

daanq =""" /* 
33201
Abhishek Mundada
N-queens Problem 
*/

#include<bits/stdc++.h>
using namespace std;

void print(int n,int col[])     // Function to print current states of Queens
{
        for(int i=0;i<n;i++)
        {
               for(int j=0;j<n;j++)
               {
                        /* Print current queen number ie row number if 
                        column matches with j else print 0 */
                        if(col[i]==j) cout<<i+1<<" ";
                        else cout<<"0 ";
               }
               cout<<"";
        }
        cout<<"";      
}


bool place(int queen,int c,int col[])      // Function to check can Queen placed at current position
{
        int j=0;
        // Iterate throgh the column array
        while(j<queen)
        {
                // Check if there is queen in same column or diagonal
                if(col[j]==c || abs(col[j]-c)==abs(j-queen))    
                        return false;
                j++;
        }
        // Return true if current position is safe
        return true;
}

bool nqueen(int queen,int n,int col[])  
{
        // Flag to check can current queen be placed in any column
        int fl=0;
        
        // Loop through all the columns
        for(int i=0;i<n;i++)
        {
                // Check can queen be placed in current column
                if(place(queen,i,col))
                {
                        // If queen can be placed then assign its column in col array 
                        col[queen]=i;   
                        
                        //Print current state
                        cout<<"Placing Queen "<<queen+1<<"";
                        print(n,col);
                        
                        //If all queens placed end the execution
                        if(queen==n-1) return true;
                        
                        //After placing current queen check if next queen can be placed in next row
                        if(nqueen(queen+1,n,col))
                                return true;
                        
                        //Backtrack if placing queen doesn't lead to solution
                        col[queen]=-1;
                        
                        //Print backtrack state
                        cout<<"Backtracking Queen "<<queen+1<<"";
                        print(n,col);
                        
                       
                        fl=1;
                }
                        
        }       
        
        //If current Queen doesnt get ant position as safe 
        if(!fl)
        cout<<"Unable to place Queen "<<queen+1<<"";
        
        return false;
}



int main()
{
        int n;
        // Input for size of chessboard
        cout<<"Enter Size of chessboard : ";
        cin>>n;
        
        // N queens can not be placed if size is less than 3
        if(n<=3)
        {
                cout<<"Size should be more than 3";
                return 0;
        }
        
        /* Initialise col array to store column number 
         of queen number same as row number */
        int col[n];
        for(int i=0;i<n;i++) col[i]=-1;
        
        // Call nqueen function to place queens 
        nqueen(0,n,col);
          
        return 0;
}

/**

************ OUTPUT for 4 * 4 ChessBoard ********************

abhishek@abhishek-Inspiron-5570:~/Desktop/DAA$ g++ nqueen.cpp
abhishek@abhishek-Inspiron-5570:~/Desktop/DAA$ ./a.out
Enter Size of chessboard : 4
Placing Queen 1
1 0 0 0 
0 0 0 0 
0 0 0 0 
0 0 0 0 

Placing Queen 2
1 0 0 0 
0 0 2 0 
0 0 0 0 
0 0 0 0 

Unable to place Queen 3

Backtracking Queen 2
1 0 0 0 
0 0 0 0 
0 0 0 0 
0 0 0 0 

Placing Queen 2
1 0 0 0 
0 0 0 2 
0 0 0 0 
0 0 0 0 

Placing Queen 3
1 0 0 0 
0 0 0 2 
0 3 0 0 
0 0 0 0 

Unable to place Queen 4

Backtracking Queen 3
1 0 0 0 
0 0 0 2 
0 0 0 0 
0 0 0 0 

Backtracking Queen 2
1 0 0 0 
0 0 0 0 
0 0 0 0 
0 0 0 0 

Backtracking Queen 1
0 0 0 0 
0 0 0 0 
0 0 0 0 
0 0 0 0 

Placing Queen 1
0 1 0 0 
0 0 0 0 
0 0 0 0 
0 0 0 0 

Placing Queen 2
0 1 0 0 
0 0 0 2 
0 0 0 0 
0 0 0 0 

Placing Queen 3
0 1 0 0 
0 0 0 2 
3 0 0 0 
0 0 0 0 

Placing Queen 4
0 1 0 0 
0 0 0 2 
3 0 0 0 
0 0 4 0 

abhishek@abhishek-Inspiron-5570:~/Desktop/DAA$ 

**/


"""

daatsp ="""#include <bits/stdc++.h> 
using namespace std; 

int all_visited;

int tsp(int mask, int pos, vector<vector<int> > adj , int dp[][50], int n)
{
	if(mask==all_visited)
	{
		//Assumption : 0th vertex as start vertex
		return adj[pos][0];
	}

	if(dp[mask][pos]!=-1) return dp[mask][pos];


	int minCost=9999999;
	for(int city=0;city<n;city++)
	{
		//If current city is not visited
		if((mask & (1<<city)) == 0)
		{
			//Find cost by visiting current city
			int cost = adj[pos][city] + tsp(mask|(1<<city),city,adj,dp,n);
			
			//Take minimum among all
			minCost=min(cost,minCost);
		}
	}	
	//Return the minimum cost 
	return dp[mask][pos]=minCost;
}



//Function to trace the path
void path(int mask,int pos,vector<vector<int> > adj , int dp[][50], int n)
{
    if(mask==all_visited) return;

    int ans = INT_MAX, chosenCity;

    for(int city=0;city<n;city++)
    {
        if((mask&(1<<city))==0)
        {
            int newAns = adj[pos][city] + dp[mask|(1<<city)][city];
            if(newAns < ans){
                ans = newAns;
                chosenCity = city;
            }
        }
    }

    // Here you get the current city you need to visit
    cout<<chosenCity+1<<"-->"; 
    path(mask|(1<<chosenCity),chosenCity,adj,dp,n);
}

//Function to validate the edges
int validate(int source, int dest,int vertices,vector<vector<int> > edge_list,int weight)
{
	if(source<0 || source>=vertices || dest<0 || dest>=vertices)
	{
		cout<<"Invalid source or destination ...";
		return 0;
	}	

	//Check for same edge in edge list
	if(edge_list[source][dest]==weight)
	{
		cout<<"Same edge alreay exists ... ";
		return 0;
	}

	return 1;
}


int main()
{
	freopen("input.txt", "r", stdin);
	freopen("output1.txt", "w", stdout);


	int vertices,edges;
	cin>>vertices>>edges;

	int n = vertices;

	vector<vector<int> > adj;

	for(int i=0;i<n;i++)
	{
		vector<int> v;
		for(int j=0;j<n;j++)
		{
			v.push_back(0);
		}
		adj.push_back(v);
	}

	
	for(int i=0;i<edges;i++)
    {
        int first_node,second_node,weight;
        cin >> first_node >> second_node >> weight;
        if(!validate(first_node-1,second_node-1,n,adj,weight))
        {
        	cout<<first_node<<" "<<second_node<<" "<<weight;
        	return 0;
        }
        adj[first_node-1][second_node-1] = weight;
    }

    int dp[(1<<n)][50];
    memset(dp,-1,sizeof(dp));

    int mask=1;

    all_visited = (1<<n)-1;
    tsp(mask,0,adj,dp,n);
    cout<<"Minimum Cost : "<< dp[1][0]<<" ";

    mask=1;

    cout<<"Path : 1-->";
    path(mask,0	,adj,dp,n);
    cout<<1<<" ";

	return 0;
}

/*

Input:

4 12
1 2 10
1 3 15
1 4 20
2 1 5
2 3 6
2 4 10
3 1 6 
3 2 13
3 4 12
4 1 8
4 2 8
4 3 9

output:
Minimum Cost : 35
Path : 1-->2-->4-->3-->1

*/"""

daatspbb= """ //TSP using Branch and Bound

#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <cstring>
#include <climits>
using namespace std;

// N is number of total nodes on the graph or the cities in the map
#define N 5

// Sentinal value for representing infinity
#define INF INT_MAX

// State Space Tree nodes
struct Node
{
    // stores edges of state space tree
    // helps in tracing path when answer is found
    vector<pair<int, int>> path;

    // stores the reduced matrix
    int reducedMatrix[N][N];

    // stores the lower bound
    int cost;

    //stores current city number
    int vertex;

    // stores number of cities visited so far
    int level;
};

// Function to allocate a new node (i, j) corresponds to visiting
// city j from city i
Node* newNode(int parentMatrix[N][N], vector<pair<int, int>> const &path,
            int level, int i, int j)
{
    Node* node = new Node;

    // stores ancestors edges of state space tree
    node->path = path;
    // skip for root node
    if (level != 0)
        // add current edge to path
        node->path.push_back(make_pair(i, j));

    // copy data from parent node to current node
    memcpy(node->reducedMatrix, parentMatrix,
        sizeof node->reducedMatrix);

    // Change all entries of row i and column j to infinity
    // skip for root node
    for (int k = 0; level != 0 && k < N; k++)
    {
        // set outgoing edges for city i to infinity
        node->reducedMatrix[i][k] = INF;

        // set incoming edges to city j to infinity
        node->reducedMatrix[k][j] = INF;
    }

    // Set (j, 0) to infinity
    // here start node is 0
    node->reducedMatrix[j][0] = INF;

    // set number of cities visited so far
    node->level = level;

    // assign current city number
    node->vertex = j;

    // return node
    return node;
}

// Function to reduce each row in such a way that
// there must be at least one zero in each row
int rowReduction(int reducedMatrix[N][N], int row[N])
{
    // initialize row array to INF
    fill_n(row, N, INF);

    // row[i] contains minimum in row i
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (reducedMatrix[i][j] < row[i])
                row[i] = reducedMatrix[i][j];

    // reduce the minimum value from each element in each row
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (reducedMatrix[i][j] != INF && row[i] != INF)
                reducedMatrix[i][j] -= row[i];
}

// Function to reduce each column in such a way that
// there must be at least one zero in each column
int columnReduction(int reducedMatrix[N][N], int col[N])
{
    // initialize col array to INF
    fill_n(col, N, INF);

    // col[j] contains minimum in col j
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (reducedMatrix[i][j] < col[j])
                col[j] = reducedMatrix[i][j];

    // reduce the minimum value from each element in each column
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            if (reducedMatrix[i][j] != INF && col[j] != INF)
                reducedMatrix[i][j] -= col[j];
}

// Function to get the lower bound on
// on the path starting at current min node
int calculateCost(int reducedMatrix[N][N])
{
    // initialize cost to 0
    int cost = 0;

    // Row Reduction
    int row[N];
    rowReduction(reducedMatrix, row);

    // Column Reduction
    int col[N];
    columnReduction(reducedMatrix, col);

    // the total expected cost
    // is the sum of all reductions
    for (int i = 0; i < N; i++)
        cost += (row[i] != INT_MAX) ? row[i] : 0,
            cost += (col[i] != INT_MAX) ? col[i] : 0;

    return cost;
}

// print list of cities visited following least cost
void printPath(vector<pair<int, int>> const &list)
{
    for (int i = 0; i < list.size(); i++)
        cout << list[i].first + 1 << " -> "
             << list[i].second + 1 << endl;
}

// Comparison object to be used to order the heap
struct comp {
    bool operator()(const Node* lhs, const Node* rhs) const
    {
        return lhs->cost > rhs->cost;
    }
};

// Function to solve Traveling Salesman Problem using Branch and Bound
int solve(int costMatrix[N][N])
{
    // Create a priority queue to store live nodes of search tree;
    priority_queue<Node*, std::vector<Node*>, comp> pq;

    vector<pair<int, int>> v;

    // create a root node and calculate its cost
    // The TSP starts from first city i.e. node 0
    Node* root = newNode(costMatrix, v, 0, -1, 0);

    // get the lower bound of the path starting at node 0
    root->cost = calculateCost(root->reducedMatrix);

    // Add root to list of live nodes;
    pq.push(root);

    // Finds a live node with least cost, add its children to list of
    // live nodes and finally deletes it from the list
    while (!pq.empty())
    {
        // Find a live node with least estimated cost
        Node* min = pq.top();

        // The found node is deleted from the list of live nodes
        pq.pop();

        // i stores current city number
        int i = min->vertex;

        // if all cities are visited
        if (min->level == N - 1)
        {
            // return to starting city
            min->path.push_back(make_pair(i, 0));

            // print list of cities visited;
            printPath(min->path);

            // return optimal cost
            return min->cost;
        }

        // do for each child of min
        // (i, j) forms an edge in space tree
        for (int j = 0; j < N; j++)
        {
            if (min->reducedMatrix[i][j] != INF)
            {
                // create a child node and calculate its cost
                Node* child = newNode(min->reducedMatrix, min->path,
                    min->level + 1, i, j);

                /* Cost of the child =
                    cost of parent node +
                    cost of the edge(i, j) +
                    lower bound of the path starting at node j
                */
                child->cost = min->cost + min->reducedMatrix[i][j]
                            + calculateCost(child->reducedMatrix);

                // Add child to list of live nodes
                pq.push(child);
            }
        }

        // free node as we have already stored edges (i, j) in vector.
        // So no need for parent node while printing solution.
        delete min;
    }
}

// main function
int main()
{
    // cost matrix for traveling salesman problem.
    /*
    int costMatrix[N][N] =
    {
        {INF, 5,   INF, 6,   5,   4},
        {5,   INF, 2,   4,   3,   INF},
        {INF, 2,   INF, 1,   INF, INF},
        {6,   4,   1,   INF, 7,   INF},
        {5,   3,   INF, 7,   INF, 3},
        {4,   INF, INF, INF, 3,   INF}
    };
    */
    // cost 34
    int costMatrix[N][N] =
    {
        { INF, 10,  8,   9,   7 },
        { 10,  INF, 10,  5,   6 },
        { 8,   10,  INF, 8,   9 },
        { 9,   5,   8,   INF, 6 },
        { 7,   6,   9,   6,   INF }
    };

    /*
    // cost 16
    int costMatrix[N][N] =
    {
        {INF, 3,   1,   5,   8},
        {3,   INF, 6,   7,   9},
        {1,   6,   INF, 4,   2},
        {5,   7,   4,   INF, 3},
        {8,   9,   2,   3,   INF}
    };
    */

    /*
    // cost 8
    int costMatrix[N][N] =
    {
        {INF, 2,   1,   INF},
        {2,   INF, 4,   3},
        {1,   4,   INF, 2},
        {INF, 3,   2,   INF}
    };
    */

    /*
    // cost 12
    int costMatrix[N][N] =
    {
        {INF, 5,   4,   3},
        {3,   INF, 8,   2},
        {5,   3,   INF, 9},
        {6,   4,   3,   INF}
    };
    */

    cout << "  Total Cost is " << solve(costMatrix);

    return 0;
}
"""

daabf = """ #include <bits/stdc++.h> 
using namespace std; 

//Recursive function to trace the path from vertex s to vertex d 
void print_path(int s,int d,vector<int> &parent)
{
	if(parent[d] == d ){
		cout<<d;
		return;
	}
	print_path(s,parent[d],parent);
	cout<<"->"<<d;
}

//Function to implement Bellman Ford Shortest pathth algorithm
int bellman_ford(vector<int> &dist,vector<int> &parent,vector<pair<int,pair<int,int> > > edge_list,int n,int source)
{
	//Assign source distance 0
	dist[source]=0;

	for(int i=1;i<=n-1;i++)
	{
		int done=1;
		for(auto j:edge_list)
		{
			/* edge.first = source
			*  edge.second.first = destination 
			*  edge.second.second = weight
			*/
			int u,v,weight;
			u=j.first, v = j.second.first , weight = j.second.second;

			//If shorter distance is present for vectex [v] then update
			if(dist[u]!=INT_MAX && dist[v] > dist[u] + weight)
			{
				done=0;
				dist[v] = dist[u]+ weight;
				parent[v]=u;
			}
		}
		if(done)
			break;
	} 

	//Loop to check whetehe there exists negative weight cycle
	for(auto j:edge_list)
	{
		int u,v,weight;
		u=j.first, v = j.second.first , weight = j.second.second;

		//If distance of any vertex is changing then there exists negative loop
		if(dist[u]!=INT_MAX && dist[v] > dist[u] + weight)
		{
			return 0;
		}
	}

	return 1;
}

//Function to validate the edges
int validate(int source, int dest,int vertices,vector<pair<int, pair<int,int> > > edge_list)
{
	if(source<1 || source>vertices || dest<1 || dest>vertices)
	{
		cout<<"Invalid source or destination ... ";
		return 0;
	}	

	//Check for same edge in edge list
	for(int i=0;i<edge_list.size();i++)
	{
		if(source==edge_list[i].first && dest==edge_list[i].second.first)
		{
			cout<<"Duplicate edge found ... ";
			return 0;
		}
	}

	return 1;
}

int main()
{
	freopen("input.txt", "r", stdin);
    freopen("output1.txt", "w", stdout);

    int vertices,edges;
   
    cin>>vertices>>edges;

    vector<pair<int,int> > adj[vertices+1];
    vector<pair<int, pair<int,int> > > edge_list;

    while(edges--)
    {
    	int source,dest,weight;
    	cin>>source>>dest>>weight;
    	if(!validate(source,dest,vertices,edge_list))
    	{
    		return 0;
    	}
    	adj[source].push_back({dest,weight});
    	edge_list.push_back({source,{dest,weight}});
    }

    //Vector to store distances of vertices from source
    vector<int> dist(vertices+1);	

    vector<int> parent(vertices+1);

    //Initialise with Infinity
    for(int i=0;i<=vertices;i++)
    	dist[i]=INT_MAX,parent[i]=i;


    if(bellman_ford(dist, parent, edge_list, vertices, 1))
    {
	    for(int i=2;i<=vertices;i++)
	    {
	    	cout<<"path from 1 to "<<i<<" : ";
	    	print_path(1,i,parent);
	    	cout<<endl;
	    	cout<<"Min Distance: "<<dist[i];
	    	cout<<"  ";
	    }
	    
    }else {
    	cout<<"Negative weight cycle exists ";
    }

    return 0;
}

/*
Input & Output : 


1)No negative weight cycle

7 10
1 2 6
1 3 5
1 4 5
3 2 -2
4 3 -2
3 5 1 
2 5 -1
4 6 -1
6 7 3
5 7 3

Output : 

path from 1 to 2 : 1->4->3->2
Min Distance: 1

path from 1 to 3 : 1->4->3
Min Distance: 3

path from 1 to 4 : 1->4
Min Distance: 5

path from 1 to 5 : 1->4->3->2->5
Min Distance: 0

path from 1 to 6 : 1->4->6
Min Distance: 4

path from 1 to 7 : 1->4->3->2->5->7
Min Distance: 3

2) Negative weight Cycle
7 10
1 2 6
1 3 5
1 4 5
3 2 -2
4 3 -2
5 3 1 
2 5 -1
4 6 -1
6 7 3
5 7 3


Output : 

Negative weight cycle exists


*/

"""

def asg1():
    print(ass1)

def asg2():
    print(ass2)

def asg3():
    print(ass3)

def asg4():
    print(ass4)

def asg5():
    print(ass5)
def daa1():
    print(daatsp)
def daa2():
    print(daabf)
def daa3():
    print(daatspbb)
def daa4():
    print(daanq)
def daa5():
    print(daaks)
