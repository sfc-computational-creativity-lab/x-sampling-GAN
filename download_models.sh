echo "getting trained model of Spoken Digits Data"
mkdir models/sc09/
wget https://s3.amazonaws.com/wavegan-v1/models/sc09.ckpt.index -O models/sc09/model.ckpt.index
wget https://s3.amazonaws.com/wavegan-v1/models/sc09.ckpt.data-00000-of-00001 -O models/sc09/model.ckpt.data-00000-of-00001
wget https://s3.amazonaws.com/wavegan-v1/models/sc09_infer.meta -O models/sc09/infer.meta
echo "getting trained model of TIMIT Speech Data"
mkdir models/timit/
wget https://s3.amazonaws.com/wavegan-v1/models/timit.ckpt.index -O models/timit/model.ckpt.index
wget https://s3.amazonaws.com/wavegan-v1/models/timit.ckpt.data-00000-of-00001 -O models/timit/model.ckpt.data-00000-of-00001
wget https://s3.amazonaws.com/wavegan-v1/models/timit_infer.meta -O models/timit/infer.meta
echo "getting trained model of Bird Data"
mkdir models/birds/
wget https://s3.amazonaws.com/wavegan-v1/models/birds.ckpt.index -O models/birds/model.ckpt.index
wget https://s3.amazonaws.com/wavegan-v1/models/birds.ckpt.data-00000-of-00001 -O models/birds/model.ckpt.data-00000-of-00001
wget https://s3.amazonaws.com/wavegan-v1/models/birds_infer.meta -O models/birds/infer.meta
echo "getting trained model of Drums Data"
mkdir models/drums/
wget https://s3.amazonaws.com/wavegan-v1/models/drums.ckpt.index -O models/drums/model.ckpt.index
wget https://s3.amazonaws.com/wavegan-v1/models/drums.ckpt.data-00000-of-00001 -O models/drums/model.ckpt.data-00000-of-00001
wget https://s3.amazonaws.com/wavegan-v1/models/drums_infer.meta -O models/drums/infer.meta
echo "getting trained model of Piano Data"
mkdir models/piano/
wget https://s3.amazonaws.com/wavegan-v1/models/piano.ckpt.index -O models/piano/model.ckpt.index
wget https://s3.amazonaws.com/wavegan-v1/models/piano.ckpt.data-00000-of-00001 -O models/piano/model.ckpt.data-00000-of-00001
wget https://s3.amazonaws.com/wavegan-v1/models/piano_infer.meta -O models/piano/infer.meta