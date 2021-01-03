from fireside import Fireside

sender = Fireside(
	name='sender1', 
	pub_address='tcp://0.0.0.0:5000', 
	sub_address='tcp://0.0.0.0:5001', 
	mode='server'
)

sender.main()