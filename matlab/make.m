mex_opts = ['-outdir mex', ' -I', fullfile(pwd, '../include')];
mex_opts = [mex_opts, ' -V'];
src1 = dir('mex/*.cpp'); src1={src1.name};
src2 = dir('mex/*.c');   src2={src2.name}; 
src3 = dir('mex/*.cc');  src3={src3.name}; 
src=[src1,src2,src3];
for i=1:length(src)
  eval(['mex ', mex_opts, ' ', fullfile('mex',src{i})]);
end


