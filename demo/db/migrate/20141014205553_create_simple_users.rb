class CreateSimpleUsers < ActiveRecord::Migration
  def change
    create_table :simple_users do |t|
      t.integer :simple_department_id

      t.timestamps
    end
  end
end
