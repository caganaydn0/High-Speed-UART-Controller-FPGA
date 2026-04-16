library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity top_module is
    generic ( 
        c_clk_freq : integer := 96_000_000;
        c_baudrate  : integer := 12_000_000
    );
    port ( 
        clk               : in  STD_LOGIC;
        rd_uart, wr_uart  : in  STD_LOGIC;
        rx_i              : in  STD_LOGIC;
        reset             : in  STD_LOGIC;
        w_data            : in  std_logic_vector(7 downto 0);
        tx_full, rx_empty : out STD_LOGIC;
        tx_o              : out STD_LOGIC;
        r_data            : out STD_LOGIC_vector(7 downto 0) 
    );         
end top_module;

architecture Behavioral of top_module is


    component uart_rx is
        generic ( 
            c_clk_freq : integer := 96_000_000;
            c_baudrate  : integer := 12_000_000
        );
        port ( 
            clk            : in  STD_LOGIC;
            rx_i           : in  STD_LOGIC;
            dout_o         : out std_logic_vector(7 downto 0);
            rx_done_tick_o : out STD_LOGIC
        );
    end component;

    component uart_tx is                               
        generic (                                          
            c_clkfreq  : integer := 96_000_000;               
            c_baudrate : integer := 12_000_000;                  
            c_stopbit  : integer := 2                          
        );                                                 
        port (                                             
            clk            : in  std_logic;                             
            din_i          : in  std_logic_vector(7 downto 0);        
            tx_start_i     : in  std_logic;                        
            tx_o           : out std_logic;                            
            tx_done_tick_o : out std_logic                     
        );                                                 
    end component;                                     

    component fifo_generator_0
        port (                                                                              
            clk   : IN  STD_LOGIC;                                                               
            srst  : IN  STD_LOGIC;                                                              
            din   : IN  STD_LOGIC_VECTOR(7 DOWNTO 0); 
            wr_en : IN  STD_LOGIC;                                                             
            rd_en : IN  STD_LOGIC;                                                             
            dout  : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);                                          
            full  : OUT STD_LOGIC;                                                             
            empty : OUT STD_LOGIC                                                             
        );                                                                                
    end component;

    component fifo_generator_1
        port (                                                                              
            clk   : IN  STD_LOGIC;                                                               
            srst  : IN  STD_LOGIC;                                                              
            din   : IN  STD_LOGIC_VECTOR(7 DOWNTO 0); 
            wr_en : IN  STD_LOGIC;                                                             
            rd_en : IN  STD_LOGIC;                                                             
            dout  : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);                                          
            full  : OUT STD_LOGIC;                                                             
            empty : OUT STD_LOGIC                                                             
        );                                                                                
    end component;
    
    component clk_wiz_0
        port (
            reset      : in std_logic;
            clk_in1    : in std_logic;
            clk_out1   : out std_logic;
            locked     : out std_logic
        );
    end component;    

      
    --RECEİVER--
    signal rx_dout         : std_logic_vector(7 downto 0) := (others => '0');
    signal rx_done_tick    : std_logic                    := '0';
    
    --TRANSMİTTER--
    signal tx_done_tick    : std_logic                    := '0';
    signal tx_start        : std_logic                    := '0';

    -- FIFO_1--
    signal fifo1_dout      : std_logic_vector(7 downto 0) := (others => '0');
    signal fifo1_empty     : std_logic                    := '1';
    signal fifo1_rd_en     : std_logic                    := '0';
    
    --FIFO_2--
    signal fifo2_din       : std_logic_vector(7 downto 0)  := (others => '0');
    signal fifo2_dout      : std_logic_vector(7 downto 0)  := (others => '0');
    signal fifo2_wr_en     : std_logic                     := '0';
    signal fifo2_empty     : std_logic                     := '1';
    signal fifo2_full      : std_logic                     := '0';
    
    signal tx_busy         : std_logic                    := '0';
    
    --CLOCK_WİZARD--
    signal clk_96MHZ       : std_logic;
    signal locked          : std_logic;

    --STM_1--
    type transfer_state_type is (IDLE, READ_FIFO1, WRITE_FIFO2);
    signal transfer_state : transfer_state_type := IDLE;
    
    --STM_2--
    type tx_state_type is (TX_IDLE, TX_SENDING);
    signal tx_state : tx_state_type := TX_IDLE;

begin

    receiver_i : uart_rx           
        generic map (                                                                                          
            c_clk_freq     => c_clk_freq,   
            c_baudrate     => c_baudrate                                                               
        )                                          
        port map (                                 
            clk            => clk_96MHZ,        
            rx_i           => rx_i,       
            dout_o         => rx_dout,       
            rx_done_tick_o => rx_done_tick
        );

    fifo_1_rx : fifo_generator_0
        port map (                                    
            clk   => clk_96MHZ,          
            srst  => reset, 
            din   => rx_dout,
            wr_en => rx_done_tick,
            rd_en => fifo1_rd_en,
            dout  => fifo1_dout,
            full  => open,   
            empty => fifo1_empty
        );                                                                     

    fifo_2_tx : fifo_generator_1 
        port map (
            clk   => clk_96MHZ,         
            srst  => reset,       
            din   => fifo1_dout,
            wr_en => fifo2_wr_en,
            rd_en => tx_done_tick,   
            dout  => fifo2_dout,
            full  => fifo2_full,        
            empty => fifo2_empty   
        );

    transmitter_i : uart_tx  
        generic map(                                                                        
            c_clkfreq  => c_clk_freq,       
            c_baudrate => c_baudrate,    
            c_stopbit  => 1               
        )  
        port map (
            clk            => clk_96MHZ,        
            din_i          => fifo2_dout,
            tx_start_i     => tx_start,
            tx_o           => tx_o,
            tx_done_tick_o => tx_done_tick
        ); 
        

  clk_wiz_0_clk_wiz_inst  : clk_wiz_0
  
  port map (
        clk_out1                  => clk_96MHZ,
        reset                     => reset,    
        locked                    => locked,   
        clk_in1                   => clk       
      );                       


    process(clk_96MHZ)
    begin
        if rising_edge(clk_96MHZ) then
            if (reset = '1' and locked = '0') then
                transfer_state <= IDLE;
                fifo1_rd_en    <= '0';
                fifo2_wr_en    <= '0';
                fifo2_din      <= (others => '0');
            else
                fifo1_rd_en <= '0';
                fifo2_wr_en <= '0';

                case transfer_state is

                    when IDLE =>
                        if fifo1_empty = '0' and fifo2_full = '0' then
                            fifo1_rd_en    <= '1';
                            transfer_state <= READ_FIFO1;
                        end if;

                    when READ_FIFO1 =>
                        transfer_state <= WRITE_FIFO2;

                    when WRITE_FIFO2 =>
                        fifo2_din      <= fifo1_dout;
                        fifo2_wr_en    <= '1';
                        transfer_state <= IDLE;

                    when others =>
                        transfer_state <= IDLE;

                end case;
            end if;
        end if;
    end process;
    process(clk_96MHZ)
    begin
        if rising_edge(clk_96MHZ) then
            if (reset = '1' and locked = '0') then
                tx_start  <= '0';
                tx_busy   <= '0';
                tx_state  <= TX_IDLE;
            else
                tx_start <= '0'; 

                case tx_state is

                    when TX_IDLE =>
                        if fifo2_empty = '0' then
                            tx_start  <= '1';
                            tx_busy   <= '1';
                            tx_state  <= TX_SENDING;
                        end if;

                    when TX_SENDING =>
                        if tx_done_tick = '1' then
                            --if fifo2_empty = '0' then
                            --tx_start <= '1';
                            --else
                                tx_busy  <= '0';
                                tx_state <= TX_IDLE;
                            end if;
                        --end if;

                   when others =>
                        tx_state <= TX_IDLE;

                end case;
            end if;
        end if;
    end process;


    r_data   <= fifo1_dout;
    rx_empty <= fifo1_empty;
    tx_full  <= fifo2_full;

end Behavioral;


-- 1.Latency Timer'ı 1ms yap (OLMUYO)
-- 2.Baud rate'i 16,000,000 olarak güncelle ($96/6$).
-- 3.Python tarafında veriyi read(65536) gibi çok büyük bloklar halinde çekmeye çalış.



