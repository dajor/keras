
python prepare_data.py --data_dir 44/

python train.py --field vendor_name --batch_size 16 
python train.py --field invoice_date --batch_size 16 
python train.py --field invoice_number --batch_size 16 
python train.py --field total_amount --batch_sizei 16 
python train.py --field net_amount --batch_size 16 
python train.py --field tax_amount --batch_size 16 
