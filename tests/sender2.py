from fireside import Fireside

sender = Fireside(
	name='sender2', 
	pub_address='tcp://0.0.0.0:5000', 
	sub_address='tcp://0.0.0.0:5001'
)

sender.main()