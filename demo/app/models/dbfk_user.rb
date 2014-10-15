class DbfkUser < ActiveRecord::Base
  belongs_to :dbfk_department, :dependent => :delete
end
