class SimpleKeyValuesController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @kvp = SimpleKeyValue.new(simplekeyvalue_params)
      @kvp.save!
      puts @kvp.id
      render json: @kvp

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def update
    @kvp = SimpleKeyValue.find(params[:key])
    @kvp.update(simplekeyvalue_params)
  end

  def update_key
    @kvp = SimpleKeyValue.find_by(key: simplekeyvalue_params[:key])
    if @kvp
      @kvp.update!(simplekeyvalue_params)
      render plain: "Success!"
    else
      render plain: "ERROR: nil"
    end
  end

  def get_key
    @kvp = SimpleKeyValue.find_by(key: simplekeyvalue_params[:key])
    if @kvp
      render json: @kvp
    else
      render plain: "ERROR: nil"
    end
  end

  def destroy_key
    @nrec  = SimpleKeyValue.destroy_all(key: simplekeyvalue_params[:key])
    render plain: "Destroyed "+@nrec.to_s
  end

  def delete_key
    @nrec  = SimpleKeyValue.delete_all(key: simplekeyvalue_params[:key])
    render plain: "Destroyed "+@nrec.to_s
  end

  def index
    render json: SimpleKeyValue.all()
  end

  def destroy
    begin
      SimpleKeyValue.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

  def destroy_all
    begin
      SimpleKeyValue.find_by_key(params[:key]) do |r| 
        r.destroy_all
      end
    end
  end


private
  def simplekeyvalue_params
    params.require(:simple_key_value).permit(:key, :value, :id)
  end
end
