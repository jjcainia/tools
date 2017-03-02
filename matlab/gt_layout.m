function [ layout ] = gt_layout( im, gt, stroke, color )
%  Layout binary groundtruth on image
%  im:     image
%  gt:     ground-truth (binary map of the same size with image)
%  stroke: stroke width (default=2)
%  color:  layout color ([255, 0, 0] for red)

if nargin <3
   color = [255, 0, 0];
   stroke = 2;
end

if nargin < 4
   color = [255, 0, 0]; 
end

assert(size(im, 1) == size(gt, 1) && size(im, 2) == size(gt, 2));
[w, h, ~] = size(im);

layout = im;
gt(bwdist(gt) < stroke) = 1;
gt = logical(gt);

[y, x] = find(gt);

for i = 1:length(y)
    y1 = y(i); x1 = x(i);
    layout(y1, x1, :) = color;
end


end

