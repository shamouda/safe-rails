class CreateSimpleDepartments < ActiveRecord::Migration
  def change
    create_table :simple_departments do |t|

      t.timestamps
    end
  end
end
