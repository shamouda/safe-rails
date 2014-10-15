class SimpleDepartmentsController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @department = SimpleDepartment.new(department_params)
      @department.id = department_params[:id]
      @department.save!
      puts @department.id
      render json: @department

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def destroy
    begin
      SimpleDepartment.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

private
  def department_params
    params.require(:simple_department).permit(:id) 
  end
end
