#include "mex.hpp"
#include <cmath>
#include <vector>
#include <string.h>
using std::vector;

double abs(double x){
	if(x>=0) return x;
	else return -x;
}

void mexFunction(MEX_ARGS){
	if (nrhs!=2) mexErrMsgTxt("Need 2 arguments");
	if (nlhs>1) mexErrMsgTxt("one output at most");
	if (!mxIsDouble(prhs[0]))mexErrMsgTxt("require double");
	if (!mxIsDouble(prhs[1]))mexErrMsgTxt("require double");
	double* im = (double*)mxGetData(prhs[0]);
	double* theta = (double*)mxGetData(prhs[1]);
    int h = mxGetM(prhs[0]);  int w = mxGetN(prhs[0]); 
    plhs[0] = mxCreateDoubleMatrix(h, w, mxREAL);
    double* out=(double*)mxGetData(plhs[0]);
    vector<double> theta1(w*h, -1);
    for (int i=0; i<w*h; ++i) theta1[i] = fmod(theta[i]+PI/double(2), PI);
    vector<int> mask(w*h, 1);
    // case 1
    vector<int> idx; idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=0)&&(theta1[y+x*h]<(PI/4))\
            &&(x<(w-1))&&(y<(h-1)));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan(theta1[id]);
    	double right = im[id+h];
    	double right_bottom = im[id+h+1];
    	double next = right*(1-d) + right_bottom*d;
    	if (im[id] < next) mask[id] = 0;
    }
    //case5
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=0)&&(theta1[y+x*h]<(PI/4))\
            &&(x>0)&&(y>0));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan(theta1[id]);
    	double left = im[id-h];
    	double left_top = im[id-h-1];
    	double next = left*(1-d) + left_top*d;

    	if (im[id] < next) mask[id] = 0;
    }
    // case 2
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=(PI/4))&&(theta1[y+x*h]<(PI/2))\
            &&(x<(w-1))&&(y<(h-1)));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan((PI/2)-theta1[id]);
    	double bottom = im[id+1];
    	double right_bottom = im[id+h+1];
    	double next = bottom*(1-d) + right_bottom*d;

    	if (im[id] < next) mask[id] = 0;
    }
    //case6
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=(PI/4))&&(theta1[y+x*h]<(PI/2))\
            &&(x>0)&&(y>0));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan((PI/2)-theta1[id]);
    	double top = im[id-1];
    	double left_top = im[id-h-1];
    	double next = top*(1-d) + left_top*d;

    	if (im[id] < next) mask[id] = 0;
    }
    // case 3
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=(PI/2))&&(theta1[y+x*h]<(3*PI/4))\
            &&(x>0)&&(y<(h-1)));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan(theta1[id]-(PI/2));
    	double bottom = im[id+1];
    	double left_bottom = im[id-h+1];
    	double next = bottom*(1-d) + left_bottom*d;

    	if (im[id] < next) mask[id] = 0;
    }
    //case7
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=(PI/2))&&(theta1[y+x*h]<(3*PI/4))\
            &&(x<(w-1))&&(y>0));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan(theta1[id]-(PI/2));
    	double top = im[id-1];
    	double right_top = im[id+h-1];
    	double next = top*(1-d) + right_top*d;

    	if (im[id] < next) mask[id] = 0;
    }
    // case 4
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=(3*PI/4))&&(theta1[y+x*h]<(PI))\
            &&(x>0)&&(y<(h-1)));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan(PI-theta1[id]);
    	double left = im[id-h];
    	double left_bottom = im[id-h+1];
    	double next = left*(1-d) + left_bottom*d;
    	if (im[id] < next) mask[id] = 0;
    }
    //case8
    idx.clear();
    for (int x=0; x<w; ++x) {
    	for (int y=0; y<h; ++y) {
            bool cond = ((theta1[y+x*h]>=(3*PI/4))&&(theta1[y+x*h]<(PI))\
            &&(x<(w-1))&&(y>0));
            if (cond){
            	//mexPrintf("%d, %d, %f\n", y, x, theta[y+x*h]);
            	idx.push_back(y+x*h);
            }
    	}
    }
    for (int i=0; i<idx.size(); ++i) {
    	int id=idx[i];
    	double d = tan(PI-theta1[id]);
    	double right = im[id+h];
    	double right_top = im[id+h-1];
    	double next = right*(1-d) + right_top*d;
    	if (im[id] < next) mask[id] = 0;
    }
    for (int i=0; i<w*h; ++i)
    	out[i] = mask[i] * im[i];
}