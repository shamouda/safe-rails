class BelongsToDepartment < ActiveRecord::Base
  has_many :belongs_to_users
end
