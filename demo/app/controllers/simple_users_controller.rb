class SimpleUsersController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @user = SimpleUser.new(user_params)
      @user.simple_department_id = user_params[:simple_department_id]
      @user.save!
      puts @user.id
      render json: @user

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def destroy
    begin
      SimpleUser.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

private
  def user_params
    params.require(:simple_user).permit(:id, :simple_department_id) 
  end
end
