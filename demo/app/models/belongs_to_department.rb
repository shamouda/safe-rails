class BelongsToDepartment < ActiveRecord::Base
  has_many :belongs_to_users, :dependent => :destroy
end
